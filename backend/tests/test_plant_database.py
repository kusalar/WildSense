import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app
from database import SessionLocal
from models import PlantRecord, SessionRecord
from services.plant_service import PlantService

client = TestClient(app)


def test_database_species_count_exceeds_100():
    """Verify botanical database contains 100+ species."""
    db = SessionLocal()
    try:
        count = db.query(PlantRecord).count()
        assert count >= 100, f"Expected at least 100 species, found {count}"
    finally:
        db.close()


def test_sessions_table_preserved():
    """Verify user session journal records are preserved safely."""
    db = SessionLocal()
    try:
        session_count = db.query(SessionRecord).count()
        assert session_count >= 34, f"Existing session records must not be lost, found {session_count}"
    finally:
        db.close()


def test_plant_taxonomy_integrity():
    """Verify all species have complete taxonomic and descriptive fields."""
    db = SessionLocal()
    try:
        plants = db.query(PlantRecord).all()
        for p in plants:
            assert p.id, "Plant must have id"
            assert p.scientific_name, f"Plant {p.id} must have scientific_name"
            assert p.canonical_name, f"Plant {p.id} must have canonical_name"
            assert p.family, f"Plant {p.id} must have family"
            assert p.genus, f"Plant {p.id} must have genus"
            assert p.category, f"Plant {p.id} must have category"
            assert len(p.distinguishing_characteristics) > 10, f"Plant {p.id} missing traits"
            assert len(p.safety_notes) > 5, f"Plant {p.id} missing safety notes"
    finally:
        db.close()


def test_regional_names_presence():
    """Verify Hindi and Bengali regional names are populated across the flora database."""
    db = SessionLocal()
    try:
        plants = [p.to_dict() for p in db.query(PlantRecord).all()]
        hindi_count = sum(1 for p in plants if "hi" in p.get("regional_names", {}) and p["regional_names"]["hi"])
        bengali_count = sum(1 for p in plants if "bn" in p.get("regional_names", {}) and p["regional_names"]["bn"])

        assert hindi_count >= 80, f"Expected majority of plants to have Hindi names, found {hindi_count}"
        assert bengali_count >= 80, f"Expected majority of plants to have Bengali names, found {bengali_count}"
    finally:
        db.close()


def test_api_list_plants():
    """Test GET /api/plants endpoint."""
    response = client.get("/api/plants?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 20
    assert "scientific_name" in data[0]
    assert "canonical_name" in data[0]
    assert "common_names" in data[0]


def test_api_categories():
    """Test GET /api/plants/categories endpoint."""
    response = client.get("/api/plants/categories")
    assert response.status_code == 200
    data = response.json()
    categories = {item["category"] for item in data}
    assert "medicinal" in categories
    assert "flower" in categories
    assert "tree" in categories


def test_api_plant_detail():
    """Test GET /api/plants/{id} endpoint."""
    response = client.get("/api/plants/ocimum-tenuiflorum")
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_name"] == "Ocimum tenuiflorum"
    assert "Tulsi" in data["common_names"] or "Holy Basil" in data["common_names"]
    assert any("तुलसी" in n for n in data["regional_names"].get("hi", []))
    assert any("তুলসী" in n for n in data["regional_names"].get("bn", []))


def test_api_search_english():
    """Test search endpoint with English query."""
    response = client.get("/api/plants/search?q=neem")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["id"] == "azadirachta-indica"


def test_api_search_bengali_script():
    """Test search endpoint with Bengali script."""
    response = client.get("/api/plants/search?q=নিম")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["id"] == "azadirachta-indica"


def test_api_search_hindi_script():
    """Test search endpoint with Hindi Devanagari script."""
    response = client.get("/api/plants/search?q=गुलाब")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert "rosa" in results[0]["genus"].lower()


def test_api_match_endpoint():
    """Test GET /api/plants/match/{name} endpoint."""
    response = client.get("/api/plants/match/Nelumbo nucifera")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "nelumbo-nucifera"
