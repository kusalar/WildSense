"""Genuine local botanical image recognition using ONNX Runtime.

Model: BioCLIP 2.5 distilled FastViT mobile student (fp32 ONNX).
Official source: crazedcodernate/bioclip-2.5-mobile-fastvit (NSF Imageomics / TreeOfLife).
License: MIT.
Classes: 4,271 verified plant species (kingdom Plantae from iNaturalist 2021).
Pretrained strictly for botanical identification; zero cloud calls.
"""

from typing import Dict, Any, List, Optional, Tuple
import os
import io
import time
import json
import logging
import numpy as np
from PIL import Image, ImageStat
from pathlib import Path

from services.vision_provider import VisionProvider

logger = logging.getLogger("wildsense.onnx_botany")

MODEL_DIR = Path(__file__).resolve().parent.parent / "models_onnx"
ONNX_MODEL_PATH = MODEL_DIR / "flora_student_fp32.onnx"
TAXA_TABLE_PATH = MODEL_DIR / "taxa_table.npy"
TAXA_LABELS_PATH = MODEL_DIR / "taxa_labels.json"

IMAGE_SIZE = 224
CROP_RESIZE = int(IMAGE_SIZE * 1.14)  # 256 for 224 center-crop

ORGAN_GUIDANCE: Dict[str, Dict[str, str]] = {
    "leaf": {
        "label": "Leaf",
        "tip": "Photograph a single leaf close-up with clear venation. Avoid heavy shadows and cluttered backgrounds.",
        "preferred_category": "leaf"
    },
    "flower": {
        "label": "Flower",
        "tip": "Photograph open petals, center disc/stamen in sharp focus and diffuse daylight.",
        "preferred_category": "flower"
    },
    "fruit": {
        "label": "Fruit",
        "tip": "Photograph mature fruit, berry, or seed capsule with clear surface detail.",
        "preferred_category": "plant"
    },
    "bark": {
        "label": "Bark",
        "tip": "Photograph trunk surface from 1-2 paces, showing vertical fissures and texture.",
        "preferred_category": "tree"
    },
    "whole_plant": {
        "label": "Whole Plant",
        "tip": "Frame the full plant habit from base to crown in its natural growth setting.",
        "preferred_category": "plant"
    }
}


def assess_image_quality(image: Image.Image) -> Dict[str, Any]:
    """Perform deterministic image quality checks prior to inference.
    Checks resolution, exposure extremes, and image contrast/variance.
    Does NOT treat mild brightness or contrast alone as proof that an image is unsuitable.
    """
    width, height = image.size
    is_low_res = width < 64 or height < 64

    # Exposure check
    rgb_im = image.convert("RGB")
    stat = ImageStat.Stat(rgb_im)
    mean_brightness = sum(stat.mean) / 3.0

    # Severe thresholds
    is_severe_underexposed = mean_brightness < 15.0
    is_severe_overexposed = mean_brightness > 245.0
    is_mild_underexposed = 15.0 <= mean_brightness < 30.0
    is_mild_overexposed = 225.0 < mean_brightness <= 245.0

    # Contrast / blurriness check via grayscale variance
    gray_stat = ImageStat.Stat(image.convert("L"))
    variance = gray_stat.var[0] if gray_stat.var else 0.0
    is_blank_or_no_detail = variance < 10.0
    is_mild_low_contrast = 10.0 <= variance < 30.0

    # Color distribution / vegetation signal check
    # Check green channel dominance / variance for conservative botanical heuristic
    r_mean, g_mean, b_mean = stat.mean[0], stat.mean[1], stat.mean[2]
    tot_mean = r_mean + g_mean + b_mean + 1e-6
    g_ratio = g_mean / tot_mean

    warnings = []
    if is_low_res:
        warnings.append(f"Low resolution ({width}x{height}px); morphological features may be compressed.")
    if is_severe_underexposed:
        warnings.append("Severe underexposure; deep shadow obscures morphological venation.")
    elif is_mild_underexposed:
        warnings.append("Subdued lighting; closer diffuse illumination recommended.")
    if is_severe_overexposed:
        warnings.append("Severe overexposure; bright washout has flattened surface texture.")
    elif is_mild_overexposed:
        warnings.append("High surface glare; consider angling camera away from direct glare.")
    if is_blank_or_no_detail:
        warnings.append("Near-zero detail or blank surface; optical features indistinct.")
    elif is_mild_low_contrast:
        warnings.append("Mild optical softness; close-up autofocus recommended.")

    if variance < 25.0 and g_ratio < 0.28:
        warnings.append("Low vegetation variation; if this is an inert object or stone, plant classification is uncertain.")

    # Phase 3A: Do not treat brightness or contrast alone as proof that an image is unsuitable.
    # Image is deemed unacceptable only if physical unreadability occurs (e.g. low resolution < 64px).
    is_acceptable = not is_low_res

    return {
        "width": width,
        "height": height,
        "brightness": round(mean_brightness, 1),
        "variance": round(variance, 1),
        "acceptable": is_acceptable,
        "warnings": warnings
    }



def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image to match official BioCLIP mobile FastViT student specs:
    1. RGB conversion
    2. Resize to 256 with bicubic interpolation
    3. Center-crop to 224x224
    4. Normalize pixel values to [0.0, 1.0] float32 NCHW tensor (1, 3, 224, 224)
    (ImageNet mean & std normalization is performed inside the ONNX graph by ExportWrapper).
    """
    im = image.convert("RGB")
    w, h = im.size

    # Maintain aspect ratio resize to CROP_RESIZE on the shorter edge
    if w < h:
        new_w = CROP_RESIZE
        new_h = int(h * (CROP_RESIZE / w))
    else:
        new_h = CROP_RESIZE
        new_w = int(w * (CROP_RESIZE / h))

    im = im.resize((new_w, new_h), Image.Resampling.BICUBIC)

    # Center crop 224x224
    left = (new_w - IMAGE_SIZE) // 2
    top = (new_h - IMAGE_SIZE) // 2
    right = left + IMAGE_SIZE
    bottom = top + IMAGE_SIZE
    im = im.crop((left, top, right, bottom))

    # Float32 normalized to [0, 1] in NCHW format
    arr = np.array(im, dtype=np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))  # HWC -> CHW
    tensor = np.expand_dims(arr, axis=0)  # -> (1, 3, 224, 224)
    return np.ascontiguousarray(tensor)


class ONNXBotanicalVisionProvider(VisionProvider):
    """Local, offline botanical classifier using ONNX Runtime with BioCLIP mobile student."""

    def __init__(
        self,
        model_path: Path = ONNX_MODEL_PATH,
        taxa_table_path: Path = TAXA_TABLE_PATH,
        taxa_labels_path: Path = TAXA_LABELS_PATH,
        enable_specialist: Optional[bool] = None
    ):
        self._model_path = model_path
        self._taxa_table_path = taxa_table_path
        self._taxa_labels_path = taxa_labels_path
        self._session = None
        self._taxa_table: Optional[np.ndarray] = None
        self._taxa_labels: Optional[List[Dict[str, Any]]] = None

        from config import ENABLE_INDIAN_FLORA_SPECIALIST
        self._enable_specialist = ENABLE_INDIAN_FLORA_SPECIALIST if enable_specialist is None else enable_specialist
        from services.specialist_arbitrator import SpecialistArbitrator
        self._arbitrator = SpecialistArbitrator()

    @property
    def provider_name(self) -> str:
        return "onnx_bioclip_botany"

    @property
    def model_name(self) -> str:
        return "BioCLIP-FastViT-4271 (fp32 ONNX)"

    @property
    def specialist_available(self) -> bool:
        return self._arbitrator.is_available()

    @property
    def specialist_enabled(self) -> bool:
        return self._enable_specialist

    @specialist_enabled.setter
    def specialist_enabled(self, val: bool):
        self._enable_specialist = bool(val)

    async def is_available(self) -> bool:
        """Check if ONNX model and taxonomy files are present on disk."""
        return (
            self._model_path.exists()
            and self._taxa_table_path.exists()
            and self._taxa_labels_path.exists()
        )

    def _load_engine(self):
        """Lazy-load the ONNX runtime session and taxonomy matrix in memory."""
        if self._session is not None:
            return

        import onnxruntime as ort

        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 2
        opts.inter_op_num_threads = 1
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self._session = ort.InferenceSession(
            str(self._model_path),
            sess_options=opts,
            providers=["CPUExecutionProvider"]
        )

        self._taxa_table = np.load(str(self._taxa_table_path))
        # Ensure float32 for clean cosine dot product
        if self._taxa_table.dtype != np.float32:
            self._taxa_table = self._taxa_table.astype(np.float32)

        with open(self._taxa_labels_path, "r", encoding="utf-8") as f:
            self._taxa_labels = json.load(f)

        logger.info(f"Loaded ONNX botanical model with {len(self._taxa_labels)} species taxa.")

    def _cross_reference_database(self, scientific_name: str) -> Optional[Dict[str, Any]]:
        """Cross-reference model's predicted scientific binomial with WildSense's 114 DB."""
        try:
            from database import SessionLocal
            from services.plant_service import PlantService
            from models import PlantRecord
            db = SessionLocal()
            try:
                plant = PlantService.get_plant_by_scientific_name(db, scientific_name)
                if plant:
                    return {
                        "match_level": "exact",
                        "database_record": plant
                    }

                # Try genus search
                genus = scientific_name.split()[0] if " " in scientific_name else scientific_name
                candidates = PlantService.search_plants(db, query_str=genus, limit=1)
                if candidates and candidates[0]["genus"].lower() == genus.lower():
                    return {
                        "match_level": "genus",
                        "database_record": candidates[0]
                    }

                return None
            finally:
                db.close()
        except Exception as e:
            logger.debug(f"Database lookup skipped: {e}")
            return None

    def _enrich_candidate(self, sci_name: str, score: float, rank: int) -> Dict[str, Any]:
        """Cross-reference a candidate taxon with the local botanical encyclopedia."""
        db_match = self._cross_reference_database(sci_name)
        match_level = "uncatalogued"
        display_common = None
        regional_names = {}
        family = None
        database_id = None

        if db_match:
            rec = db_match["database_record"]
            match_level = db_match.get("match_level", "uncatalogued")
            family = rec.get("family")
            database_id = rec.get("id")
            c_names = rec.get("common_names", [])
            regional_names = rec.get("regional_names", {})

            if match_level == "exact":
                display_common = c_names[0] if c_names else rec.get("canonical_name")
            elif match_level == "genus":
                genus = rec.get("genus")
                display_common = f"{c_names[0]} group" if c_names else f"{genus} genus"

        return {
            "rank": rank,
            "scientific_name": sci_name,
            "common_name": display_common,
            "regional_names": regional_names,
            "similarity_score": round(score, 3),
            "cosine_score": round(score, 3),  # Backward compatibility
            "match_level": match_level,
            "family": family,
            "database_id": database_id
        }

    async def analyze_image(self, image_bytes: bytes, organ_type: Optional[str] = None) -> Dict[str, Any]:
        """Classify single plant specimen photo using pure local ONNX inference."""
        return await self.analyze_images([image_bytes], organ_type=organ_type)

    async def analyze_images(
        self,
        images_bytes: List[bytes],
        organ_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Classify plant specimen supporting 1 to 3 photos of the same specimen,
        organ type selection, and L2-normalized embedding aggregation.
        """
        t0 = time.perf_counter()
        self._load_engine()

        # Sanitize organ_type
        clean_organ = (organ_type or "whole_plant").strip().lower()
        if clean_organ not in ORGAN_GUIDANCE:
            clean_organ = "whole_plant"
        organ_info = ORGAN_GUIDANCE.get(clean_organ, ORGAN_GUIDANCE["whole_plant"])

        if not images_bytes:
            return {
                "category": "other",
                "common_name": "No Image Provided",
                "confidence": 0.0,
                "similarity_score": 0.0,
                "description": "No image data was submitted for recognition.",
                "uncertainty": "Zero image bytes provided.",
                "provider": self.provider_name,
                "inference_ms": int((time.perf_counter() - t0) * 1000),
                "organ_type": clean_organ,
                "photos_count": 0,
                "candidates": []
            }

        # Cap at 3 photos
        images_bytes = images_bytes[:3]

        valid_embeddings = []
        individual_results = []
        overall_quality_warnings = []
        last_quality = None

        for idx, b in enumerate(images_bytes):
            try:
                img = Image.open(io.BytesIO(b))
            except Exception as e:
                individual_results.append({
                    "photo_index": idx + 1,
                    "scientific_name": "Unreadable",
                    "similarity_score": 0.0,
                    "match_level": "error",
                    "quality_warnings": [f"Unreadable image data: {e}"]
                })
                continue

            quality = assess_image_quality(img)
            last_quality = quality
            overall_quality_warnings.extend(quality["warnings"])

            if not quality["acceptable"]:
                individual_results.append({
                    "photo_index": idx + 1,
                    "scientific_name": "Poor Quality",
                    "similarity_score": 0.0,
                    "match_level": "rejected",
                    "quality_warnings": quality["warnings"]
                })
                continue

            # Extract normalized embedding
            tensor = preprocess_image(img)
            outputs = self._session.run(None, {"image": tensor})
            emb = outputs[0]  # shape: (1, 1024)
            # Re-verify L2 norm
            norm = np.linalg.norm(emb, axis=-1, keepdims=True)
            emb = emb / np.maximum(norm, 1e-9)
            valid_embeddings.append(emb)

            # Compute individual photo top candidate for transparency
            indiv_sims = (emb @ self._taxa_table.T)[0]
            top_indiv_idx = int(np.argmax(indiv_sims))
            indiv_sci = self._taxa_labels[top_indiv_idx].get("scientific", "")
            indiv_score = float(indiv_sims[top_indiv_idx])
            indiv_db = self._cross_reference_database(indiv_sci)
            indiv_match_lvl = indiv_db.get("match_level", "uncatalogued") if indiv_db else "uncatalogued"

            individual_results.append({
                "photo_index": idx + 1,
                "scientific_name": indiv_sci,
                "similarity_score": round(indiv_score, 3),
                "match_level": indiv_match_lvl,
                "quality_warnings": quality["warnings"]
            })

        if not valid_embeddings:
            # All photos failed or were unreadable
            return {
                "category": "other",
                "common_name": "Unreadable Specimen Photo",
                "scientific_name": None,
                "confidence": 0.0,
                "similarity_score": 0.0,
                "raw_cosine": 0.0,
                "description": "None of the provided images had sufficient optical quality for botanical recognition.",
                "uncertainty": "Image quality check failed. Ensure photos are sharp, in focus, and well-lit.",
                "provider": self.provider_name,
                "inference_ms": int((time.perf_counter() - t0) * 1000),
                "organ_type": clean_organ,
                "photos_count": len(images_bytes),
                "individual_photos": individual_results,
                "image_quality": {
                    "acceptable": False,
                    "warnings": overall_quality_warnings or ["Images could not be decoded."]
                },
                "arbitration": {
                    "enabled": self._enable_specialist,
                    "decision": "optical_rejection",
                    "use_specialist": False
                },
                "candidates": []
            }

        # Multi-photo embedding combination
        if len(valid_embeddings) == 1:
            combined_emb = valid_embeddings[0]
            aggregation_method = "single_photo"
        else:
            # Mean aggregation of L2-normalized unit vectors
            summed = np.sum(valid_embeddings, axis=0)
            combined_norm = np.linalg.norm(summed, axis=-1, keepdims=True)
            combined_emb = summed / np.maximum(combined_norm, 1e-9)
            aggregation_method = "mean_l2_normalized"

        # Cosine similarity matrix multiplication against all 4,271 plant taxa
        similarities = (combined_emb @ self._taxa_table.T)[0]

        # Top 5 species candidates
        top_indices = np.argsort(similarities)[-5:][::-1]
        top_candidates = []
        for rank, idx in enumerate(top_indices):
            entry = self._taxa_labels[idx]
            sci_name = entry.get("scientific", "")
            score = float(similarities[idx])
            top_candidates.append(self._enrich_candidate(sci_name, score, rank + 1))

        best_cand = top_candidates[0]
        best_sci = best_cand["scientific_name"]
        raw_score = best_cand["similarity_score"]
        second_score = top_candidates[1]["similarity_score"] if len(top_candidates) > 1 else raw_score
        margin = round(raw_score - second_score, 3)
        category = organ_info["preferred_category"]

        # Dual scoring & Indian Flora Specialist Arbitration (behind feature flag)
        arbitration_diag = {
            "enabled": self._enable_specialist,
            "decision": "disabled" if not self._enable_specialist else "evaluated",
            "chosen_source": "global",
            "use_specialist": False
        }

        if self._enable_specialist and self._arbitrator.is_available():
            arb = self._arbitrator.arbitrate(combined_emb, top_candidates, last_quality or {})
            arbitration_diag = arb
            if arb.get("use_specialist"):
                best_sci = arb["specialist_candidate"]
                raw_score = arb["specialist_score"]
                second_score = top_candidates[0]["similarity_score"]
                margin = arb.get("specialist_margin", 0.0)
                match_level = arb.get("match_level", "exact")
                spec_info = arb.get("specialist_info", {})
                if spec_info and spec_info.get("category"):
                    category = spec_info.get("category", category)

                # Prepend specialist candidate to candidates list for transparency
                spec_cand = {
                    "rank": 1,
                    "scientific_name": best_sci,
                    "common_name": spec_info.get("common_name", best_sci),
                    "regional_names": spec_info.get("regional_names", {}),
                    "similarity_score": round(raw_score, 3),
                    "cosine_score": round(raw_score, 3),
                    "match_level": match_level,
                    "family": spec_info.get("family"),
                    "source": "specialist"
                }
                top_candidates = [spec_cand] + [
                    {**c, "rank": c["rank"] + 1} for c in top_candidates[:4]
                ]
                if arb.get("warnings"):
                    overall_quality_warnings.extend(arb["warnings"])

        # Honest categorization & match level
        match_level = best_cand["match_level"] if not arbitration_diag.get("use_specialist") else arbitration_diag.get("match_level", "exact")
        db_match = self._cross_reference_database(best_sci)

        common_name = best_sci
        description = f"Specimen matches morphological features of {best_sci}."

        if db_match and db_match.get("match_level") == "exact":
            rec = db_match["database_record"]
            category = rec.get("category", organ_info["preferred_category"])
            c_names = rec.get("common_names", [])
            hi_names = rec.get("regional_names", {}).get("hi", [])
            bn_names = rec.get("regional_names", {}).get("bn", [])
            primary_name = c_names[0] if c_names else rec["canonical_name"]

            display_vernacular = []
            if hi_names:
                display_vernacular.append(f"हिन्दी: {hi_names[0]}")
            if bn_names:
                display_vernacular.append(f"বাংলা: {bn_names[0]}")
            vernacular_str = f" ({', '.join(display_vernacular)})" if display_vernacular else ""

            common_name = f"{primary_name} ({best_sci})"
            description = (
                f"{rec.get('description', '')} "
                f"Distinguishing traits: {rec.get('distinguishing_characteristics', '')[:160]}"
            )
            match_details = (
                f"Verified botanical database match: {rec['canonical_name']} ({rec['family']}). "
                f"Similarity score: {raw_score:.2f}."
            )
        elif db_match and db_match.get("match_level") == "genus":
            rec = db_match["database_record"]
            genus = rec["genus"]
            c_names = rec.get("common_names", [])
            primary_name = c_names[0] if c_names else genus
            common_name = f"{best_sci} ({primary_name} / {genus} group)"
            match_details = (
                f"Genus match with local encyclopedia ({genus}). "
                f"Predicted species {best_sci} belongs to the genus of {rec['canonical_name']}."
            )
        else:
            common_name = best_sci
            match_details = (
                f"Identified from 4,271 global botanical taxa; full local dossier not yet indexed in 114-species core. "
                f"Similarity score: {raw_score:.2f}."
            )

        # Epistemic calibration & uncertainty reporting
        # Label as similarity, not certitude
        if raw_score >= 0.70 and margin >= 0.02:
            calibrated_conf = min(0.85, max(0.65, raw_score))
            uncertainty = (
                f"High botanical similarity ({raw_score:.2f}, margin: {margin:+.2f}). "
                f"Morphological features align with {best_sci}."
            )
        elif raw_score >= 0.58:
            calibrated_conf = min(0.64, max(0.48, raw_score * 0.9))
            uncertainty = (
                f"Moderate similarity ({raw_score:.2f}, margin: {margin:+.2f}). "
                f"Lookalikes or regional varieties likely. "
                f"Submitting an additional photo of a different plant organ (e.g. flower or leaf) can clarify ambiguous traits."
            )
        else:
            calibrated_conf = min(0.45, max(0.15, raw_score * 0.7))
            common_name = f"Uncertain: possibly {best_sci}"
            uncertainty = (
                f"Weak botanical similarity ({raw_score:.2f}, margin: {margin:+.2f}). "
                f"Target may be an uncatalogued regional plant, occluded, or non-plant object. "
                f"We recommend retaking a close-up photo with better lighting focusing on leaf or petal details."
            )

        if overall_quality_warnings:
            uncertainty += f" (Note: {overall_quality_warnings[0]})"

        inference_ms = int((time.perf_counter() - t0) * 1000)

        # Deduplicate warnings
        unique_warnings = list(dict.fromkeys(overall_quality_warnings))

        return {
            "category": category,
            "common_name": common_name,
            "scientific_name": best_sci,
            "similarity_score": round(raw_score, 3),
            "confidence": round(calibrated_conf, 2),
            "raw_cosine": round(raw_score, 3),  # Backward compatibility
            "match_level": match_level,
            "match_details": match_details,
            "organ_type": clean_organ,
            "organ_tip": organ_info["tip"],
            "photos_count": len(valid_embeddings),
            "aggregation": aggregation_method,
            "individual_photos": individual_results,
            "description": description.strip(),
            "uncertainty": uncertainty.strip(),
            "candidates": top_candidates,
            "inference_ms": inference_ms,
            "provider": self.provider_name,
            "image_quality": {
                "width": last_quality["width"] if last_quality else 224,
                "height": last_quality["height"] if last_quality else 224,
                "brightness": last_quality["brightness"] if last_quality else 128.0,
                "variance": last_quality["variance"] if last_quality else 50.0,
                "acceptable": True,
                "warnings": unique_warnings
            },
            "arbitration": arbitration_diag
        }
