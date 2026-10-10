import sys
from pathlib import Path
import pytest
import numpy as np
from PIL import Image

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from services.onnx_botany_provider import (
    ONNXBotanicalVisionProvider,
    preprocess_image,
    assess_image_quality
)
from services.recognizer import ObjectRecognizer
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_onnx_provider_availability():
    """Verify ONNX model files and runtime are available."""
    provider = ONNXBotanicalVisionProvider()
    import asyncio
    is_avail = asyncio.run(provider.is_available())
    assert is_avail is True, "ONNX botanical model should be available locally"


def test_image_preprocessing():
    """Verify image preprocessing matches expected shape (1, 3, 224, 224) and range [0, 1]."""
    img = Image.new("RGB", (640, 480), color=(120, 200, 80))
    tensor = preprocess_image(img)
    assert tensor.shape == (1, 3, 224, 224)
    assert tensor.dtype == np.float32
    assert tensor.min() >= 0.0
    assert tensor.max() <= 1.0


def test_image_quality_diagnostics():
    """Verify image quality diagnostics detect low-res, blur, and exposure anomalies."""
    # Low resolution
    tiny_img = Image.new("RGB", (32, 32), color=(100, 100, 100))
    q_tiny = assess_image_quality(tiny_img)
    assert any("Low resolution" in w for w in q_tiny["warnings"])

    # Severe underexposure
    dark_img = Image.new("RGB", (256, 256), color=(5, 5, 5))
    q_dark = assess_image_quality(dark_img)
    assert any("underexposure" in w for w in q_dark["warnings"])

    # Normal image
    normal_img = Image.new("RGB", (300, 300), color=(100, 150, 80))
    q_normal = assess_image_quality(normal_img)
    assert q_normal["width"] == 300
    assert q_normal["height"] == 300


def test_onnx_inference_dummy_data():
    """Verify local inference runs on synthetic image and returns valid botanical schema."""
    import asyncio
    import io
    provider = ONNXBotanicalVisionProvider()
    img = Image.new("RGB", (256, 256), color=(40, 160, 40))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    result = asyncio.run(provider.analyze_image(img_bytes))
    assert "common_name" in result
    assert "scientific_name" in result
    assert "confidence" in result
    assert "candidates" in result
    assert len(result["candidates"]) == 5
    assert result["provider"] == "onnx_bioclip_botany"
    assert result["inference_ms"] > 0
    # Epistemic modesty: synthetic flat green should not have 0.99 confidence
    assert result["confidence"] <= 0.85


def test_onnx_inference_real_lotus_specimen():
    """Verify genuine lotus image classification against 4,271 botanical species."""
    import asyncio
    lotus_path = Path("test_specimens/lotus.jpg")
    if not lotus_path.exists():
        pytest.skip("Test specimen not found")

    provider = ONNXBotanicalVisionProvider()
    with open(lotus_path, "rb") as f:
        img_bytes = f.read()

    result = asyncio.run(provider.analyze_image(img_bytes))
    assert "Nelumbo" in result["scientific_name"]
    assert result["category"] == "aquatic"
    assert "Nelumbo nucifera" in result["candidates"][0]["scientific_name"]


def test_recognizer_service_priority():
    """Verify ObjectRecognizer prioritizes ONNX botanical provider for uploaded images."""
    import asyncio
    recognizer = ObjectRecognizer()
    assert asyncio.run(recognizer.is_onnx_available()) is True
    assert asyncio.run(recognizer.is_vision_available()) is True

    # Preset should still work
    preset_res = asyncio.run(recognizer.recognize(preset_id="demo_leaf"))
    assert preset_res["provider"] == "demo_preset"
    assert "Neem" in preset_res["common_name"]



def test_api_health_endpoint_reports_onnx():
    """Verify GET /api/health exposes ONNX botanical capability."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["onnx_available"] is True
    assert "BioCLIP" in data["onnx_model"]
