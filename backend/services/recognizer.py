import base64
import io
import re
from typing import Dict, Any, Optional, List
from PIL import Image
from services.vision_provider import VisionProvider, OllamaVisionProvider, MockVisionProvider
from services.onnx_botany_provider import ONNXBotanicalVisionProvider
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
    Priority order:
    1. ONNXBotanicalVisionProvider (BioCLIP FastViT mobile student, 4,271 verified plant species)
    2. OllamaVisionProvider (if local Ollama vision model installed)
    3. MockVisionProvider (local CV color & spectral fallback)
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
        self.onnx_botany = ONNXBotanicalVisionProvider()
        self.ollama_vision = vision_provider or OllamaVisionProvider(base_url=OLLAMA_BASE_URL, model=VISION_MODEL)
        self.mock_vision = MockVisionProvider(provider_name="local_cv_fallback")

    def get_presets(self) -> Dict[str, Dict[str, Any]]:
        return self.DEMO_PRESETS

    async def is_onnx_available(self) -> bool:
        """Check if local ONNX botanical model is available."""
        return await self.onnx_botany.is_available()

    async def is_vision_available(self) -> bool:
        """Check if local vision capabilities (ONNX botanical or Ollama) are available."""
        return await self.onnx_botany.is_available() or await self.ollama_vision.is_available()

    async def recognize_bytes(self, image_bytes: bytes, organ_type: Optional[str] = None) -> Dict[str, Any]:
        """Processes a single image byte stream with organ-type support."""
        return await self.recognize_multi_bytes([image_bytes], organ_type=organ_type)

    async def recognize_multi_bytes(self, images_bytes: List[bytes], organ_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes real image bytes through the vision provider chain:
        1. Genuine local ONNX Botanical classifier with L2-normalized embedding aggregation
        2. Local Ollama Vision model (if available)
        3. Local CV feature/spectral analyzer (mock vision fallback)
        4. Unknown Nature Object safety fallback
        """
        if not images_bytes:
            return {
                "category": "other",
                "common_name": "Nature Object Detected",
                "confidence": 0.50,
                "similarity_score": 0.50,
                "description": "Nature object detected — let's investigate its physical characteristics.",
                "uncertainty": "No visual data submitted; ready for real-world field investigation.",
                "provider": "fallback",
                "inference_ms": 5,
                "organ_type": organ_type or "whole_plant",
                "photos_count": 0
            }

        # 1. Try genuine local ONNX Botanical classifier first
        try:
            if await self.onnx_botany.is_available():
                return await self.onnx_botany.analyze_images(images_bytes, organ_type=organ_type)
        except Exception as e:
            logger.warning(f"ONNX botanical inference failed: {e}. Falling back to Ollama/Mock.")

        # 2. Try real Ollama vision model if available (uses first image)
        try:
            if await self.ollama_vision.is_available():
                res = await self.ollama_vision.analyze_image(images_bytes[0])
                res["organ_type"] = organ_type or "whole_plant"
                res["photos_count"] = len(images_bytes)
                return res
        except Exception as e:
            logger.warning(f"Ollama vision inference failed: {e}. Falling back to local CV.")

        # 3. Fallback to in-memory local CV analysis
        try:
            res = await self.mock_vision.analyze_image(images_bytes[0])
            res["organ_type"] = organ_type or "whole_plant"
            res["photos_count"] = len(images_bytes)
            return res
        except Exception as e:
            logger.warning(f"Mock vision analysis failed: {e}. Falling back to Unknown Object.")

        # 4. Final safety fallback
        return {
            "category": "other",
            "common_name": "Nature Object Detected",
            "confidence": 0.50,
            "similarity_score": 0.50,
            "description": "Nature object detected — let's investigate its physical characteristics.",
            "uncertainty": "Demo/fallback recognition: visual classification is approximate.",
            "provider": "fallback",
            "inference_ms": 5,
            "organ_type": organ_type or "whole_plant",
            "photos_count": len(images_bytes)
        }

    async def recognize(
        self,
        image_input: Optional[str] = None,
        preset_id: Optional[str] = None,
        organ_type: Optional[str] = None,
        images_input: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Handles legacy/demo/base64 inputs while using VisionProvider for image data.
        """
        # If demo preset requested directly
        if preset_id and preset_id in self.DEMO_PRESETS:
            preset = dict(self.DEMO_PRESETS[preset_id])
            preset["organ_type"] = organ_type or "whole_plant"
            preset["photos_count"] = 1
            return preset

        # Collect base64 inputs
        all_inputs = []
        if images_input:
            all_inputs.extend(images_input)
        elif image_input and image_input.strip():
            all_inputs.append(image_input)

        if not all_inputs:
            return {
                "category": "other",
                "common_name": "Nature Object Detected",
                "confidence": 0.50,
                "similarity_score": 0.50,
                "description": "Nature object detected — let's investigate its physical characteristics.",
                "uncertainty": "No visual data submitted; ready for real-world field investigation.",
                "provider": "fallback",
                "inference_ms": 5,
                "organ_type": organ_type or "whole_plant",
                "photos_count": 0
            }

        # Check for preset token in any input string
        for inp in all_inputs:
            for key in self.DEMO_PRESETS:
                if key in inp.lower():
                    preset = dict(self.DEMO_PRESETS[key])
                    preset["organ_type"] = organ_type or "whole_plant"
                    preset["photos_count"] = len(all_inputs)
                    return preset

        # Decode base64 images
        bytes_list = []
        for inp in all_inputs:
            try:
                raw_base64 = re.sub(r"^data:image/[a-zA-Z0-9\+\-\.]+;base64,", "", inp.strip())
                b = base64.b64decode(raw_base64)
                if len(b) > 0:
                    bytes_list.append(b)
            except Exception:
                continue

        if not bytes_list:
            return {
                "category": "other",
                "common_name": "Nature Object Detected",
                "confidence": 0.55,
                "similarity_score": 0.55,
                "description": "Nature object detected — let's investigate its physical characteristics.",
                "uncertainty": "Visual classification is approximate. Investigation mission ready.",
                "provider": "fallback",
                "inference_ms": 5,
                "organ_type": organ_type or "whole_plant",
                "photos_count": 0
            }

        return await self.recognize_multi_bytes(bytes_list, organ_type=organ_type)

