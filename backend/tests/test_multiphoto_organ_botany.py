import io
import sys
from pathlib import Path
import pytest
from PIL import Image
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from main import app
from services.onnx_botany_provider import ONNXBotanicalVisionProvider, ORGAN_GUIDANCE
from services.recognizer import ObjectRecognizer

client = TestClient(app)

def create_synthetic_image(width: int = 224, height: int = 224, color=(60, 140, 60)) -> bytes:
    """Helper to create synthetic JPEG bytes."""
    im = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    im.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.mark.anyio
async def test_single_photo_compatibility():
    """Verify single-photo workflow remains 100% functional with rich Phase 2/3 metadata."""
    provider = ONNXBotanicalVisionProvider()
    assert await provider.is_available()

    img_bytes = create_synthetic_image()
    result = await provider.analyze_image(img_bytes, organ_type="leaf")

    assert "common_name" in result
    assert "scientific_name" in result
    assert "similarity_score" in result
    assert "confidence" in result
    assert "raw_cosine" in result
    assert "candidates" in result
    assert len(result["candidates"]) == 5
    assert result["photos_count"] == 1
    assert result["aggregation"] == "single_photo"
    assert result["organ_type"] == "leaf"
    assert "organ_tip" in result
    assert result["match_level"] in {"exact", "genus", "family", "uncatalogued"}
    assert "individual_photos" in result
    assert len(result["individual_photos"]) == 1


@pytest.mark.anyio
async def test_organ_type_selection():
    """Verify all 5 botanical organ types are accepted with guidance tips."""
    provider = ONNXBotanicalVisionProvider()
    img_bytes = create_synthetic_image()

    for organ in ["leaf", "flower", "fruit", "bark", "whole_plant"]:
        res = await provider.analyze_image(img_bytes, organ_type=organ)
        assert res["organ_type"] == organ
        assert res["organ_tip"] == ORGAN_GUIDANCE[organ]["tip"]


@pytest.mark.anyio
async def test_multi_photo_aggregation_and_decomposition():
    """Verify up to 3 photos are aggregated via L2-normalized mean with per-photo decomposition."""
    provider = ONNXBotanicalVisionProvider()
    
    # 2 synthetic images
    img1 = create_synthetic_image(color=(50, 150, 50))
    img2 = create_synthetic_image(color=(70, 130, 70))
    
    res = await provider.analyze_images([img1, img2], organ_type="flower")
    
    assert res["photos_count"] == 2
    assert res["aggregation"] == "mean_l2_normalized"
    assert res["organ_type"] == "flower"
    assert len(res["candidates"]) == 5
    assert "individual_photos" in res
    assert len(res["individual_photos"]) == 2
    assert res["individual_photos"][0]["photo_index"] == 1
    assert res["individual_photos"][1]["photo_index"] == 2


@pytest.mark.anyio
async def test_real_specimen_exact_and_genus_match():
    """Verify real lotus yields exact match and real rose yields genus match in candidates."""
    provider = ONNXBotanicalVisionProvider()
    lotus_path = Path("test_specimens/lotus.jpg")
    rose_path = Path("test_specimens/rose.jpg")

    if lotus_path.exists():
        with open(lotus_path, "rb") as f:
            lotus_res = await provider.analyze_image(f.read(), organ_type="flower")
        assert lotus_res["scientific_name"] == "Nelumbo nucifera"
        assert lotus_res["match_level"] == "exact"
        # Hindi/Bengali vernacular present in common_name or regional_names
        top_cand = lotus_res["candidates"][0]
        assert top_cand["match_level"] == "exact"

    if rose_path.exists():
        with open(rose_path, "rb") as f:
            rose_res = await provider.analyze_image(f.read(), organ_type="flower")
        assert rose_res["scientific_name"].startswith("Rosa ")
        assert rose_res["match_level"] == "genus"


def test_api_multipart_single_and_multi_upload():
    """Verify /api/recognize endpoint with multipart uploads (single and multiple)."""
    img1 = create_synthetic_image()
    img2 = create_synthetic_image()

    # 1. Single image multipart
    res_single = client.post(
        "/api/recognize",
        data={"organ_type": "leaf"},
        files={"image": ("test.jpg", img1, "image/jpeg")}
    )
    assert res_single.status_code == 200
    data_single = res_single.json()
    assert data_single["photos_count"] == 1
    assert data_single["organ_type"] == "leaf"
    assert "similarity_score" in data_single
    assert len(data_single["candidates"]) == 5

    # 2. Multi-photo multipart (2 files)
    res_multi = client.post(
        "/api/recognize",
        data={"organ_type": "flower"},
        files=[
            ("images", ("test1.jpg", img1, "image/jpeg")),
            ("images", ("test2.jpg", img2, "image/jpeg")),
        ]
    )
    assert res_multi.status_code == 200
    data_multi = res_multi.json()
    assert data_multi["photos_count"] == 2
    assert data_multi["aggregation"] == "mean_l2_normalized"
    assert len(data_multi["individual_photos"]) == 2


def test_api_upload_limit_enforced():
    """Verify that uploading more than 3 photos returns HTTP 400."""
    img = create_synthetic_image()
    res = client.post(
        "/api/recognize",
        files=[
            ("images", ("1.jpg", img, "image/jpeg")),
            ("images", ("2.jpg", img, "image/jpeg")),
            ("images", ("3.jpg", img, "image/jpeg")),
            ("images", ("4.jpg", img, "image/jpeg")),
        ]
    )
    assert res.status_code == 400
    assert "Maximum 3 specimen photos" in res.json()["detail"]


def test_api_invalid_file_handling():
    """Verify that corrupt or empty file uploads are handled gracefully with HTTP 400."""
    # Empty file
    res_empty = client.post(
        "/api/recognize",
        files={"image": ("empty.jpg", b"", "image/jpeg")}
    )
    assert res_empty.status_code == 400

    # Corrupt non-image
    res_corrupt = client.post(
        "/api/recognize",
        files={"image": ("bad.jpg", b"not-a-valid-image", "image/jpeg")}
    )
    assert res_corrupt.status_code == 400
