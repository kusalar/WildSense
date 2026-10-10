import base64
import io
import re
from typing import Dict, Any, Optional
from PIL import Image
from services.vision_provider import VisionProvider, OllamaVisionProvider, MockVisionProvider
from config import OLLAMA_BASE_URL, VISION_MODEL

import logging

logger = logging.getLogger("wildsense.recognizer")

CATEGORIES = [
    "plant", "leaf", "flower", "tree", "bird", "insect", "fungus", "rock", "animal", "other"
]

class ObjectRecognizer:
    """
    Pluggable nature object recognition service integrating dedicated VisionProviders
    with epistemic modesty.
    """

    DEMO_PRESETS = {
        "demo_leaf": {
            "category": "leaf",
            "common_name": "Likely Neem Leaf",
            "confidence": 0.74,
            "description": "Elongated serrated pinnate leaflet with distinct curved tip and light underside veins.",
            "uncertainty": "Visual identification is approximate; vein angles match Azadirachta genus.",
            "provider": "demo_preset",
            "inference_ms": 12
        },
        "demo_mango_leaf": {
            "category": "leaf",
            "common_name": "Appears to be a Mango Leaf",
            "confidence": 0.72,
            "description": "Lanceolate leathery blade with wavy margins and prominent central midrib.",
            "uncertainty": "Leaf morphology suggests Mangifera indica; lighting prevents cellular confirmation.",
            "provider": "demo_preset",
            "inference_ms": 14
        },
        "demo_flower": {
            "category": "flower",
            "common_name": "Wild Field Flower",
            "confidence": 0.78,
            "description": "Bright radial golden inflorescence composed of composite ray florets.",
            "uncertainty": "Radial petal symmetry suggests wild Asteraceae or dandelion; species unconfirmed.",
            "provider": "demo_preset",
            "inference_ms": 11
        },
        "demo_rock": {
            "category": "rock",
            "common_name": "Weathered Surface Rock",
            "confidence": 0.81,
            "description": "Coarse-grained weathered mineral surface harboring flat crustose lichen rings.",
            "uncertainty": "Mineral morphology suggests granite or fieldstone; exact mineralogy unverified.",
            "provider": "demo_preset",
            "inference_ms": 9
        },
        "demo_unknown_plant": {
            "category": "plant",
            "common_name": "Unidentified Understory Plant",
            "confidence": 0.58,
            "description": "Compact herbaceous understory growth with alternating blade clusters.",
            "uncertainty": "Low confidence match; specimen details partially occluded.",
            "provider": "demo_preset",
            "inference_ms": 8
        },
        "demo_tree": {
            "category": "tree",
            "common_name": "Mature Bark Trunk",
            "confidence": 0.76,
            "description": "Deeply fissured woody bark showing vertical ridges and micro-lichen colonies.",
            "uncertainty": "Bark patterns indicate mature deciduous trunk; exact canopy unseen.",
            "provider": "demo_preset",
            "inference_ms": 10
        },
        "demo_insect": {
            "category": "insect",
            "common_name": "Solitary Pollinator or Ground Beetle",
            "confidence": 0.69,
            "description": "Small segmented arthropod actively moving along vegetative substrate.",
            "uncertainty": "Movement and scale prevent exact entomological classification.",
            "provider": "demo_preset",
            "inference_ms": 15
        },
        "demo_bird": {
            "category": "bird",
            "common_name": "Perching Songbird Silhouette",
            "confidence": 0.65,
            "description": "Small passerine perched on foliage showing upright posture.",
            "uncertainty": "Distance and plumage illumination leave exact species ambiguous.",
            "provider": "demo_preset",
            "inference_ms": 16
        }
    }

    def __init__(self, vision_provider: Optional[VisionProvider] = None):
        self.ollama_vision = vision_provider or OllamaVisionProvider(base_url=OLLAMA_BASE_URL, model=VISION_MODEL)
        self.mock_vision = MockVisionProvider(provider_name="local_cv_fallback")

    def get_presets(self) -> Dict[str, Dict[str, Any]]:
        return self.DEMO_PRESETS

    async def is_vision_available(self) -> bool:
        """Check if local Ollama vision model is installed and reachable."""
        return await self.ollama_vision.is_available()

    async def recognize_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Processes real image bytes through the vision provider chain:
        1. Local Ollama Vision model (if available)
        2. Local CV feature/spectral analyzer (mock vision fallback)
        3. Unknown Nature Object safety fallback
        """
        # 1. Try real Ollama vision model first
        try:
            if await self.ollama_vision.is_available():
                return await self.ollama_vision.analyze_image(image_bytes)
        except Exception as e:
            logger.warning(f"Ollama vision inference failed: {e}. Falling back to local CV.")

        # 2. Fallback to in-memory local CV analysis
        try:
            return await self.mock_vision.analyze_image(image_bytes)
        except Exception as e:
            logger.warning(f"Mock vision analysis failed: {e}. Falling back to Unknown Object.")

        # 3. Final safety fallback
        return {
            "category": "other",
            "common_name": "Nature Object Detected",
            "confidence": 0.50,
            "description": "Nature object detected — let's investigate its physical characteristics.",
            "uncertainty": "Demo/fallback recognition: visual classification is approximate.",
            "provider": "fallback",
            "inference_ms": 5
        }

    async def recognize(self, image_input: Optional[str] = None, preset_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Handles legacy/demo/base64 inputs while using VisionProvider for image data.
        """
        # If demo preset requested directly
        if preset_id and preset_id in self.DEMO_PRESETS:
            return dict(self.DEMO_PRESETS[preset_id])

        if not image_input or image_input.strip() == "":
            return {
                "category": "other",
                "common_name": "Nature Object Detected",
                "confidence": 0.50,
                "description": "Nature object detected — let's investigate its physical characteristics.",
                "uncertainty": "No visual data submitted; ready for real-world field investigation.",
                "provider": "fallback",
                "inference_ms": 5
            }

        # Check for preset token in string
        for key in self.DEMO_PRESETS:
            if key in image_input.lower():
                return dict(self.DEMO_PRESETS[key])

        try:
            raw_base64 = re.sub(r"^data:image/.+;base64,", "", image_input.strip())
            image_bytes = base64.b64decode(raw_base64)
            return await self.recognize_bytes(image_bytes)
        except Exception:
            return {
                "category": "other",
                "common_name": "Nature Object Detected",
                "confidence": 0.55,
                "description": "Nature object detected — let's investigate its physical characteristics.",
                "uncertainty": "Visual classification is approximate. Investigation mission ready.",
                "provider": "fallback",
                "inference_ms": 5
            }
