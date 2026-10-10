"""WildSense Indian Flora Specialist Arbitration Service.

Implements dual-scoring and multi-gate arbitration between the global 4,271-class
FastViT classifier and the 7-class Indian Flora Specialist head.
Operates behind the ENABLE_INDIAN_FLORA_SPECIALIST feature flag.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

logger = logging.getLogger("wildsense.specialist_arbitrator")

# Default path to the specialist artifact
DEFAULT_SPECIALIST_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "specialist_dataset" / "indian_flora_specialist.npz"

# Development-tuned acceptance thresholds (derived strictly from train + val sets)
DEV_THRESHOLDS = {
    "Ocimum tenuiflorum": 0.680,
    "Tagetes erecta": 0.720,
    "Azadirachta indica": 0.710,
    "Nyctanthes arbor-tristis": 0.700,
    "Butea monosperma": 0.680,
    "Moringa oleifera": 0.680,
    "Rosa chinensis": 0.700
}

MIN_SPECIALIST_MARGIN = 0.035

SPECIALIST_METADATA = {
    "Ocimum tenuiflorum": {
        "genus": "Ocimum",
        "family": "Lamiaceae",
        "common_name": "Tulsi (Holy Basil)",
        "regional_names": {"hi": ["तुलसी"], "bn": ["তুলসী"], "sa": ["तुलसी"]},
        "category": "leaf",
        "description": "Sacred aromatic herb with opposite ovate serrated leaves and terminal racemes."
    },
    "Tagetes erecta": {
        "genus": "Tagetes",
        "family": "Asteraceae",
        "common_name": "African Marigold (Genda)",
        "regional_names": {"hi": ["गेंदा"], "bn": ["গাঁদা"]},
        "category": "flower",
        "description": "Popular garden and ceremonial composite flower with dense golden/orange florets and pinnate foliage."
    },
    "Azadirachta indica": {
        "genus": "Azadirachta",
        "family": "Meliaceae",
        "common_name": "Neem Tree",
        "regional_names": {"hi": ["नीम"], "bn": ["নিম"], "sa": ["निम्ब"]},
        "category": "tree",
        "description": "Resilient medicinal tree characterized by once-pinnate asymmetric serrated leaflets with curved tips."
    },
    "Nyctanthes arbor-tristis": {
        "genus": "Nyctanthes",
        "family": "Oleaceae",
        "common_name": "Shiuli / Night-flowering Jasmine",
        "regional_names": {"hi": ["हरसिंगार", "पारिजात"], "bn": ["শিউলি"], "sa": ["पारिजात"]},
        "category": "flower",
        "description": "Fragrant sacred shrub with rough opposite leaves and nocturnal white pinwheel petals with bright orange floral tubes."
    },
    "Butea monosperma": {
        "genus": "Butea",
        "family": "Fabaceae",
        "common_name": "Palash (Flame of the Forest)",
        "regional_names": {"hi": ["पलाश", "ढाक"], "bn": ["পলাশ"], "sa": ["पलाश"]},
        "category": "tree",
        "description": "Deciduous dry-season tree famed for fiery vermilion papilionaceous flowers and large trifoliate leaves."
    },
    "Moringa oleifera": {
        "genus": "Moringa",
        "family": "Moringaceae",
        "common_name": "Moringa (Drumstick Tree / Sahjan)",
        "regional_names": {"hi": ["सहजन"], "bn": ["সজনে"], "sa": ["शोभाञ्जन"]},
        "category": "tree",
        "description": "Fast-growing multipurpose tree with bi- or tripinnately compound leaves, tiny oval leaflets, and long pendulous pods."
    },
    "Rosa chinensis": {
        "genus": "Rosa",
        "family": "Rosaceae",
        "common_name": "Cultivated Rose (China Rose group)",
        "regional_names": {"hi": ["गुलाब"], "bn": ["গোলাপ"]},
        "category": "flower",
        "description": "Continuous-blooming garden rose ancestor with prickly stems, pinnate leaflets, and multi-petaled blossoms."
    }
}


class SpecialistArbitrator:
    """Manages dual-scoring and multi-gate arbitration between global and specialist classifiers."""

    def __init__(self, artifact_path: Path = DEFAULT_SPECIALIST_PATH):
        self._artifact_path = Path(artifact_path)
        self._centroids: Optional[np.ndarray] = None
        self._classes: Optional[List[str]] = None
        self._thresholds: Dict[str, float] = DEV_THRESHOLDS
        self._loaded = False

    def is_available(self) -> bool:
        """Check if specialist artifact exists on disk."""
        return self._artifact_path.exists()

    def load(self):
        """Lazy load the specialist centroid matrix."""
        if self._loaded:
            return

        if not self._artifact_path.exists():
            logger.warning(f"Specialist artifact not found at {self._artifact_path}")
            return

        data = np.load(str(self._artifact_path))
        self._centroids = data["centroids"]
        self._classes = [str(c) for c in data["classes"]]

        if "metadata" in data:
            meta = json.loads(str(data["metadata"]))
            # Use stored thresholds if present, but fallback to DEV_THRESHOLDS
            loaded_thresh = meta.get("validation_thresholds", {})
            self._thresholds = {c: loaded_thresh.get(c, DEV_THRESHOLDS.get(c, 0.70)) for c in self._classes}

        self._loaded = True
        logger.info(f"Loaded Indian Flora Specialist with {len(self._classes)} classes.")

    def score_specialist(self, embedding: np.ndarray) -> List[Dict[str, Any]]:
        """Score an embedding vector against the 7 specialist centroids."""
        self.load()
        if not self._loaded or self._centroids is None:
            return []

        # Embedding must be 1D (1024,)
        flat_emb = embedding.flatten()
        norm = np.linalg.norm(flat_emb)
        if norm > 1e-9:
            flat_emb = flat_emb / norm

        sims = flat_emb @ self._centroids.T  # (7,)
        sorted_indices = np.argsort(-sims)

        results = []
        for rank, idx in enumerate(sorted_indices):
            sci = self._classes[idx]
            score = float(sims[idx])
            info = SPECIALIST_METADATA.get(sci, {})
            results.append({
                "rank": rank + 1,
                "scientific_name": sci,
                "common_name": info.get("common_name", sci),
                "similarity_score": round(score, 3),
                "family": info.get("family"),
                "genus": info.get("genus"),
                "threshold": self._thresholds.get(sci, 0.70)
            })
        return results

    def arbitrate(
        self,
        combined_embedding: np.ndarray,
        global_candidates: List[Dict[str, Any]],
        optical_quality: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform multi-gate arbitration between global candidates and regional specialist."""
        self.load()
        if not self._loaded or not global_candidates:
            # Fallback directly to global top-1 if specialist unavailable
            return {
                "decision": "global_fallback",
                "chosen_source": "global",
                "use_specialist": False,
                "warnings": []
            }

        warnings = list(optical_quality.get("warnings", []))

        # Gate 0: Optical / Non-plant Check
        if not optical_quality.get("acceptable", True):
            return {
                "decision": "optical_rejection",
                "chosen_source": "rejected",
                "use_specialist": False,
                "warnings": warnings + ["Rejected due to physical unreadability."]
            }

        # Check for stone/inert non-plant signal
        is_inert_stone = any("inert object or stone" in w.lower() for w in warnings)
        if is_inert_stone:
            warnings.append("Low vegetation variation; potential inert object. Suppressed specialist assertion.")
            return {
                "decision": "inert_suppression",
                "chosen_source": "global",
                "use_specialist": False,
                "warnings": warnings
            }

        # 1. Global top candidate info
        best_global = global_candidates[0]
        top_g_sci = best_global.get("scientific_name", "")
        top_g_score = float(best_global.get("similarity_score", 0.0))
        top_g_genus = top_g_sci.split()[0] if " " in top_g_sci else top_g_sci

        # 2. Specialist scoring
        specialist_candidates = self.score_specialist(combined_embedding)
        if not specialist_candidates:
            return {
                "decision": "global",
                "chosen_source": "global",
                "use_specialist": False,
                "warnings": warnings
            }

        best_spec = specialist_candidates[0]
        runner_spec = specialist_candidates[1] if len(specialist_candidates) > 1 else best_spec

        top_s_sci = best_spec["scientific_name"]
        top_s_score = best_spec["similarity_score"]
        runner_s_score = runner_spec["similarity_score"]
        s_margin = round(top_s_score - runner_s_score, 3)

        threshold = self._thresholds.get(top_s_sci, 0.700)
        spec_genus = best_spec.get("genus", "")

        # Gate 3: Concordance vs Contradiction
        genus_concordance = (top_g_genus.lower() == spec_genus.lower())
        
        # If global model has high confidence (>= 0.635) on a non-specialist genus, global wins
        global_is_confident_non_specialist = (top_g_score >= 0.635) and not genus_concordance

        # Specialist Acceptance Criteria
        specialist_accepted = (
            top_s_score >= threshold and
            s_margin >= MIN_SPECIALIST_MARGIN and
            not global_is_confident_non_specialist
        )

        diagnostics = {
            "decision": "specialist" if specialist_accepted else "global",
            "chosen_source": "specialist" if specialist_accepted else "global",
            "use_specialist": specialist_accepted,
            "specialist_candidate": top_s_sci,
            "specialist_score": top_s_score,
            "specialist_runner_up": runner_spec["scientific_name"],
            "specialist_margin": s_margin,
            "specialist_threshold": threshold,
            "global_candidate": top_g_sci,
            "global_score": top_g_score,
            "genus_concordance": genus_concordance,
            "global_confident_non_spec": global_is_confident_non_specialist,
            "warnings": warnings
        }

        if specialist_accepted:
            # Confusion Handling: Tulsi vs Sweet Basil
            if top_s_sci == "Ocimum tenuiflorum":
                diagnostics["warnings"].append(
                    "Genus-level confirmation (Ocimum sp. / Holy Basil group). "
                    "Vegetative similarity with Sweet Basil (Ocimum basilicum) requires floral/calyx inspection."
                )
                diagnostics["match_level"] = "genus_confirmed"
            else:
                diagnostics["match_level"] = "exact"

            # Confusion Handling: Neem vs Moringa
            if top_s_sci in ("Azadirachta indica", "Moringa oleifera"):
                other = "Moringa oleifera" if top_s_sci == "Azadirachta indica" else "Azadirachta indica"
                other_cand = next((c for c in specialist_candidates if c["scientific_name"] == other), None)
                if other_cand and (top_s_score - other_cand["similarity_score"]) < 0.050:
                    diagnostics["warnings"].append(
                        "Foliage overlap warning: morphological overlap between Neem and Moringa leaflets; "
                        "verify leaf architecture (once-pinnate vs bi/tripinnate)."
                    )

            diagnostics["specialist_info"] = SPECIALIST_METADATA.get(top_s_sci, {})
            return diagnostics

        # Fallback to Global
        if top_g_score < 0.60:
            diagnostics["warnings"].append("Low confidence match; specimen uncatalogued or outside known flora.")
            diagnostics["match_level"] = "uncertain"
        else:
            diagnostics["match_level"] = best_global.get("match_level", "uncatalogued")

        return diagnostics
