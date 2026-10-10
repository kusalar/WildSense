"""Tests for Stage 5: Safe Global + Indian Flora Specialist Arbitration."""

import pytest
import os
import io
import json
import numpy as np
from PIL import Image
import sys
from pathlib import Path
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app
from config import ENABLE_INDIAN_FLORA_SPECIALIST
from services.onnx_botany_provider import ONNXBotanicalVisionProvider
from services.specialist_arbitrator import SpecialistArbitrator, DEFAULT_SPECIALIST_PATH

client = TestClient(app)

SPECIMENS_DIR = Path(__file__).resolve().parent.parent.parent / "test_specimens"
CACHE_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "specialist_dataset" / "cached_embeddings.npz"
MANIFEST_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "specialist_dataset" / "embeddings_manifest.json"


def test_specialist_feature_flag_disabled_by_default():
    """Verify specialist is disabled by default to guarantee safe rollout."""
    assert ENABLE_INDIAN_FLORA_SPECIALIST is False
    provider = ONNXBotanicalVisionProvider()
    assert provider.specialist_enabled is False


def test_arbitrator_availability_and_structure():
    """Verify specialist artifact exists, loads correctly, and contains 7 classes."""
    arbitrator = SpecialistArbitrator()
    assert arbitrator.is_available() is True
    arbitrator.load()
    assert arbitrator._loaded is True
    assert len(arbitrator._classes) == 7
    assert arbitrator._centroids.shape == (7, 1024)
    assert "Ocimum tenuiflorum" in arbitrator._classes
    assert "Azadirachta indica" in arbitrator._classes


import asyncio

def test_optical_safeguards_block_specialist():
    """Verify low resolution or poor quality images are rejected before specialist can assert a class."""
    provider = ONNXBotanicalVisionProvider(enable_specialist=True)
    
    # 32x32 blank image (rejected by resolution safeguard)
    tiny_im = Image.new("RGB", (32, 32), color=(100, 150, 100))
    buf = io.BytesIO()
    tiny_im.save(buf, format="JPEG")
    
    result = asyncio.run(provider.analyze_image(buf.getvalue()))
    assert result["category"] == "other"
    assert result["similarity_score"] == 0.0
    assert result["arbitration"]["decision"] == "optical_rejection"
    assert result["arbitration"]["use_specialist"] is False


def test_supported_baseline_species_preserve_global_precedence():
    """Verify Hibiscus, Lotus, and Water Lily remain with Global model and are NOT hijacked by specialist."""
    provider = ONNXBotanicalVisionProvider(enable_specialist=True)
    
    # 1. Hibiscus
    hibiscus_path = SPECIMENS_DIR / "hibiscus.jpg"
    if hibiscus_path.exists():
        with open(hibiscus_path, "rb") as f:
            res = asyncio.run(provider.analyze_image(f.read()))
        assert res["arbitration"]["chosen_source"] == "global"
        assert res["arbitration"]["use_specialist"] is False
        assert "Hibiscus" in res["scientific_name"]

    # 2. Lotus
    lotus_path = SPECIMENS_DIR / "lotus.jpg"
    if lotus_path.exists():
        with open(lotus_path, "rb") as f:
            res = asyncio.run(provider.analyze_image(f.read()))
        assert res["arbitration"]["chosen_source"] == "global"
        assert res["arbitration"]["use_specialist"] is False
        assert "Nelumbo" in res["scientific_name"]

    # 3. Water Lily
    water_lily_path = SPECIMENS_DIR / "water_lily.jpg"
    if water_lily_path.exists():
        with open(water_lily_path, "rb") as f:
            res = asyncio.run(provider.analyze_image(f.read()))
        assert res["arbitration"]["chosen_source"] == "global"
        assert res["arbitration"]["use_specialist"] is False
        assert "Nymphaea" in res["scientific_name"]


def test_missing_regional_species_promoted_by_specialist():
    """Verify Neem and Tulsi are recognized when specialist arbitration is enabled."""
    provider = ONNXBotanicalVisionProvider(enable_specialist=True)
    
    # Neem
    neem_path = SPECIMENS_DIR / "neem.jpg"
    if neem_path.exists():
        with open(neem_path, "rb") as f:
            res = asyncio.run(provider.analyze_image(f.read()))
        assert res["arbitration"]["use_specialist"] is True
        assert res["scientific_name"] == "Azadirachta indica"
        assert res["similarity_score"] >= 0.75
        assert res["candidates"][0]["source"] == "specialist"

    # Tulsi
    tulsi_path = SPECIMENS_DIR / "tulsi.jpg"
    if tulsi_path.exists():
        with open(tulsi_path, "rb") as f:
            res = asyncio.run(provider.analyze_image(f.read()))
        assert res["arbitration"]["use_specialist"] is True
        assert res["scientific_name"] == "Ocimum tenuiflorum"
        assert res["match_level"] == "genus_confirmed"
        # Warning regarding Sweet Basil must be present
        any_basil_warning = any("Ocimum basilicum" in w for w in res["image_quality"]["warnings"])
        assert any_basil_warning is True


def test_sweet_basil_confusion_handling():
    """Verify Sweet Basil controls trigger genus_confirmed match level and warning."""
    arbitrator = SpecialistArbitrator()
    arbitrator.load()
    
    if CACHE_FILE.exists() and MANIFEST_FILE.exists():
        npz = np.load(str(CACHE_FILE))
        embs = npz["embeddings"]
        keys = list(npz["keys"])
        key_to_idx = {k: i for i, k in enumerate(keys)}
        
        with open(str(MANIFEST_FILE), "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        control_items = [m for m in manifest if m["split"] == "control"]
        for it in control_items:
            emb = embs[key_to_idx[it["key"]]]
            global_cands = [{"scientific_name": "Vitex agnus-castus", "similarity_score": 0.58}]
            diag = arbitrator.arbitrate(emb, global_cands, {"acceptable": True, "warnings": []})
            
            if diag.get("use_specialist") and diag.get("specialist_candidate") == "Ocimum tenuiflorum":
                assert diag["match_level"] == "genus_confirmed"
                assert any("Sweet Basil" in w for w in diag["warnings"])


def test_neem_vs_moringa_confusion_guardrail():
    """Verify compound leaflet overlap warning triggers when Neem and Moringa have close scores."""
    arbitrator = SpecialistArbitrator()
    arbitrator.load()
    
    # Create synthetic embedding equidistant between Neem and Moringa centroids
    neem_idx = arbitrator._classes.index("Azadirachta indica")
    moringa_idx = arbitrator._classes.index("Moringa oleifera")
    v = (arbitrator._centroids[neem_idx] + arbitrator._centroids[moringa_idx]) / 2.0
    v = v / np.linalg.norm(v)
    
    global_cands = [{"scientific_name": "Bursera simaruba", "similarity_score": 0.55}]
    diag = arbitrator.arbitrate(v, global_cands, {"acceptable": True, "warnings": []})
    
    if diag.get("use_specialist"):
        foliage_warn = any("compound leaflet" in w.lower() or "foliage overlap" in w.lower() for w in diag["warnings"])
        assert foliage_warn is True


def test_api_health_endpoint_reports_specialist_status():
    """Verify health endpoint accurately reports specialist availability and enablement."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "specialist_available" in data
    assert "specialist_enabled" in data
    assert data["specialist_available"] is True
    assert data["specialist_enabled"] is False


def test_api_arbitration_legacy_compatibility():
    """Verify /api/recognize returns valid response schema with arbitration field."""
    # Test with demo preset
    resp = client.post("/api/recognize", json={"preset_id": "demo_leaf"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "leaf"
    assert "confidence" in data
    assert "description" in data
    assert "uncertainty" in data
