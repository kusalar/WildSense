import asyncio
import io
import sys
from pathlib import Path
from PIL import Image
import pytest
from fastapi.testclient import TestClient

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from main import app
from services.recognizer import ObjectRecognizer
from services.vision_provider import VisionProvider, OllamaVisionProvider, MockVisionProvider, ALLOWED_CATEGORIES
from services.mission_generator import MissionGenerator
from services.grass_score import (
    calculate_grass_score,
    calculate_ratio_score,
    calculate_mission_score,
    calculate_field_time_score,
    calculate_reflection_score,
    format_duration,
)
from services.ai_provider import MockProvider

client = TestClient(app)

def create_test_image(color=(34, 139, 34), size=(100, 100), fmt="PNG") -> bytes:
    """Helper to create valid in-memory test images."""
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=fmt)
    return buf.getvalue()


# ==========================================
# 1. Vision Provider Tests
# ==========================================

def test_vision_provider_interface():
    """Verify VisionProvider ABC enforces contract."""
    assert issubclass(OllamaVisionProvider, VisionProvider)
    assert issubclass(MockVisionProvider, VisionProvider)

    # Cannot instantiate ABC directly
    with pytest.raises(TypeError):
        # pyrefly: ignore [bad-instantiation]
        VisionProvider()


def test_mock_vision_provider():
    """Verify MockVisionProvider analyzes image bytes and returns structured schema."""
    provider = MockVisionProvider()
    assert provider.provider_name == "local_cv_fallback"
    assert asyncio.run(provider.is_available()) is True

    # Test leaf (green dominant)
    green_img = create_test_image(color=(20, 180, 40))
    res = asyncio.run(provider.analyze_image(green_img))
    assert res["category"] in ALLOWED_CATEGORIES
    assert 0.0 <= res["confidence"] <= 1.0
    assert "uncertainty" in res
    assert "inference_ms" in res
    assert res["inference_ms"] >= 0
    assert res["provider"] == "local_cv_fallback"

    # Test flower (red/warm dominant)
    flower_img = create_test_image(color=(210, 40, 110))
    res_fl = asyncio.run(provider.analyze_image(flower_img))
    assert res_fl["category"] in ALLOWED_CATEGORIES
    assert 0.0 <= res_fl["confidence"] <= 1.0


def test_unavailable_vision_model():
    """Verify OllamaVisionProvider gracefully handles an unreachable host or missing model."""
    provider = OllamaVisionProvider(base_url="http://127.0.0.1:59999", model="nonexistent_vision_model", timeout_seconds=1.0)
    assert asyncio.run(provider.is_available()) is False


def test_malformed_response_handling():
    """Verify _normalize_vision_response handles non-JSON and malformed inputs gracefully."""
    provider = OllamaVisionProvider(model="moondream")

    # Non-JSON string
    assert provider._normalize_vision_response("I see a green leaf here", 100) is None

    # Empty string
    assert provider._normalize_vision_response("", 100) is None

    # Markdown wrapped valid JSON
    markdown_json = """```json
    {
      "category": "leaf",
      "common_name": "Likely Neem Leaf",
      "confidence": 0.74,
      "description": "Elongated serrated foliage.",
      "uncertainty": "Visual identification is approximate."
    }
    ```"""
    parsed = provider._normalize_vision_response(markdown_json, 150)
    assert parsed is not None
    assert parsed["category"] == "leaf"
    assert parsed["confidence"] == 0.74
    assert parsed["inference_ms"] == 150
    assert parsed["provider"] == "ollama_vision"


def test_invalid_confidence_normalization():
    """Verify confidence values are clamped to [0.0, 1.0] and percentage strings are parsed."""
    provider = OllamaVisionProvider(model="moondream")

    # Over 1.0 float clamped
    res1 = provider._normalize_vision_response('{"category": "plant", "confidence": 1.45}', 50)
    assert res1 is not None
    assert res1["confidence"] == 1.0

    # Negative float clamped
    res2 = provider._normalize_vision_response('{"category": "rock", "confidence": -0.2}', 50)
    assert res2 is not None
    assert res2["confidence"] == 0.0

    # Percentage string parsed
    res3 = provider._normalize_vision_response('{"category": "flower", "confidence": "78%"}', 50)
    assert res3 is not None
    assert res3["confidence"] == 0.78

    # Non-numeric fallback
    res4 = provider._normalize_vision_response('{"category": "tree", "confidence": "high"}', 50)
    assert res4 is not None
    assert res4["confidence"] == 0.50


def test_low_confidence_recognition():
    """Verify low-confidence results retain epistemic modesty."""
    provider = OllamaVisionProvider(model="moondream")
    res = provider._normalize_vision_response(
        '{"category": "other", "common_name": "Unidentified Growth", "confidence": 0.41, "uncertainty": "Low clarity."}',
        50
    )
    assert res is not None
    assert res["confidence"] == 0.41
    assert "uncertainty" in res


def test_successful_structured_recognition():
    """Verify full normalization adheres to allowed categories and schema keys."""
    provider = OllamaVisionProvider(model="moondream")
    raw = '{"category": "INSECT", "common_name": "Field Beetle", "confidence": 0.69, "description": "Segmented thorax.", "uncertainty": "Approximate."}'
    res = provider._normalize_vision_response(raw, 200)
    assert res is not None
    assert res["category"] == "insect"
    assert res["common_name"] == "Field Beetle"
    assert res["confidence"] == 0.69
    assert res["provider"] == "ollama_vision"


# ==========================================
# 2. Recognizer Service Tests
# ==========================================

def test_recognizer_schema_and_epistemic_honesty():
    recognizer = ObjectRecognizer()

    # 1. Test Neem Leaf demo preset
    leaf_result = asyncio.run(recognizer.recognize(preset_id="demo_leaf"))
    assert leaf_result["category"] == "leaf"
    assert leaf_result["confidence"] == 0.74
    assert "Likely Neem" in leaf_result["common_name"]
    assert "uncertainty" in leaf_result
    assert "approximate" in leaf_result["uncertainty"].lower()

    # 2. Test unknown object fallback
    fallback_result = asyncio.run(recognizer.recognize(image_input=None))
    assert fallback_result["category"] == "other"
    assert "Nature Object Detected" in fallback_result["common_name"]
    assert "uncertainty" in fallback_result

    # 3. Test presets list
    presets = recognizer.get_presets()
    assert "demo_leaf" in presets
    assert "demo_flower" in presets
    assert "demo_rock" in presets
    assert "demo_tree" in presets
    assert "demo_unknown_plant" in presets


def test_recognizer_bytes_fallback():
    """Test recognize_bytes processes real in-memory image bytes via fallback chain."""
    recognizer = ObjectRecognizer()
    img_bytes = create_test_image(color=(30, 160, 40))
    result = asyncio.run(recognizer.recognize_bytes(img_bytes))

    assert result["category"] in ALLOWED_CATEGORIES
    assert 0.0 <= result["confidence"] <= 1.0
    assert "common_name" in result
    assert "uncertainty" in result
    assert "inference_ms" in result
    assert result["provider"] in {"ollama_vision", "local_cv_fallback", "fallback"}


# ==========================================
# 3. API Endpoints Tests
# ==========================================

def test_api_health_endpoint():
    """Verify /health endpoint exposes required vision and model status."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert "ollama_connected" in data
    assert "configured_model" in data
    assert "vision_model" in data
    assert "vision_available" in data
    assert isinstance(data["vision_available"], bool)


def test_api_demo_recognition():
    """Verify /api/recognize with demo preset continues working."""
    res = client.post("/api/recognize", json={"preset_id": "demo_flower"})
    assert res.status_code == 200
    data = res.json()
    assert data["category"] == "flower"
    assert data["confidence"] == 0.78
    assert "uncertainty" in data


def test_api_image_recognition_multipart():
    """Verify /api/recognize accepts real multipart image upload."""
    img_bytes = create_test_image(color=(35, 140, 35), fmt="PNG")
    files = {"image": ("test_foliage.png", img_bytes, "image/png")}
    res = client.post("/api/recognize", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["category"] in ALLOWED_CATEGORIES
    assert 0.0 <= data["confidence"] <= 1.0
    assert "common_name" in data
    assert "uncertainty" in data
    assert "inference_ms" in data


def test_api_invalid_image():
    """Verify /api/recognize rejects corrupt/malformed image bytes with 400."""
    corrupt_bytes = b"NOT_A_REAL_IMAGE_DATA_CORRUPTED"
    files = {"image": ("bad.png", corrupt_bytes, "image/png")}
    res = client.post("/api/recognize", files=files)
    assert res.status_code == 400
    assert "Invalid or malformed" in res.json()["detail"] or "Unsupported" in res.json()["detail"]


def test_api_empty_image():
    """Verify /api/recognize rejects 0-byte file with 400."""
    files = {"image": ("empty.png", b"", "image/png")}
    res = client.post("/api/recognize", files=files)
    assert res.status_code == 400
    assert "empty" in res.json()["detail"].lower()


def test_api_unsupported_image_type():
    """Verify /api/recognize rejects unsupported file format (e.g. text/plain) with 400."""
    files = {"image": ("notes.txt", b"hello nature notes", "text/plain")}
    res = client.post("/api/recognize", files=files)
    assert res.status_code == 400
    assert "Unsupported" in res.json()["detail"]


def test_api_fallback_behavior():
    """Verify API gracefully falls back when Ollama vision model is offline without crashing."""
    img_bytes = create_test_image(color=(128, 128, 128), fmt="JPEG")
    files = {"image": ("rock_specimen.jpg", img_bytes, "image/jpeg")}
    res = client.post("/api/recognize", files=files)
    assert res.status_code == 200
    data = res.json()
    # Must succeed and indicate local fallback or vision
    assert data["provider"] in {"local_cv_fallback", "ollama_vision", "fallback"}
    assert "approximate" in data["uncertainty"].lower()


# ==========================================
# 4. Privacy Guarantees Tests
# ==========================================

def test_privacy_guarantees():
    """Verify no external cloud URLs are generated or returned for uploaded images."""
    img_bytes = create_test_image(color=(40, 160, 40))
    files = {"image": ("private_nature.png", img_bytes, "image/png")}
    res = client.post("/api/recognize", files=files)
    assert res.status_code == 200
    data = res.json()

    # Recognition must not return a cloud URL
    for val in data.values():
        if isinstance(val, str):
            assert not val.startswith("http://") or "127.0.0.1" in val or "localhost" in val
            assert "amazonaws.com" not in val
            assert "googleapis.com" not in val
            assert "azure.com" not in val


# ==========================================
# 5. Mission & Reflection Tests
# ==========================================

def test_mission_schema_and_categories():
    generator = MissionGenerator(ai_provider=MockProvider())

    async def run_checks():
        for category in ["leaf", "flower", "tree", "rock", "insect", "bird", "fungus", "plant", "other"]:
            mission = await generator.generate_mission(
                object_name=f"Test {category}",
                category=category,
                confidence=0.75,
                available_time_minutes=2
            )
            # Check required schema keys
            assert "title" in mission
            assert "instruction" in mission
            assert "why" in mission
            assert "estimated_minutes" in mission
            assert "physical_action" in mission
            assert "observation_goal" in mission
            assert "safety_note" in mission
            assert "llm_inference_ms" in mission
            assert isinstance(mission["estimated_minutes"], int)

    asyncio.run(run_checks())


def test_mission_safety_rules_validator():
    generator = MissionGenerator()

    # Safe mission must pass
    safe_mission = {
        "title": "Leaf Detective",
        "instruction": "Look underneath the leaf and observe the veins without picking it.",
        "physical_action": "Crouch slightly.",
        "safety_note": "Do not touch unknown foliage."
    }
    assert generator.validate_safety(safe_mission) is True

    # Dangerous violations must be caught
    dangerous_cases = [
        {"instruction": "Taste the leaf to see if it is bitter.", "title": "Taste Test"},
        {"instruction": "Eat one of the wild berries.", "title": "Foraging"},
        {"instruction": "Pick the leaf and pull it off the branch.", "title": "Specimen Collection"},
        {"instruction": "Touch unknown fungus with bare hands.", "title": "Fungi Handling"},
        {"instruction": "Approach the bird's active nest and check inside.", "title": "Nest Check"},
        {"instruction": "Catch the insect in a jar.", "title": "Bug Hunt"},
        {"instruction": "Trespass over the private boundary wall.", "title": "Off trail"}
    ]

    for case in dangerous_cases:
        assert generator.validate_safety(case) is False, f"Failed to catch safety violation: {case}"

    # Verify all built-in category fallbacks are strictly safe
    for cat in generator.CATEGORY_STRATEGIES:
        fallback = generator.CATEGORY_STRATEGIES[cat]
        assert generator.validate_safety(fallback) is True, f"Category fallback {cat} failed safety validation"


def test_grass_score_ratio_component():
    """Verify ratio piecewise interpolation is monotonic, non-negative, and bounded at 70 max."""
    test_ratios = [0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 20.0, 100.0]
    prev_score = -1.0

    for r in test_ratios:
        pts = calculate_ratio_score(r)
        assert 0.0 <= pts <= 70.0, f"Ratio score {pts} out of bounds for ratio {r}"
        assert pts >= prev_score, f"Ratio score not monotonically increasing at {r}: {pts} < {prev_score}"
        prev_score = pts

    # Test exact milestone points (mapped * 0.70)
    assert calculate_ratio_score(1.0) == pytest.approx(17.5)
    assert calculate_ratio_score(3.0) == pytest.approx(38.5)
    assert calculate_ratio_score(5.0) == pytest.approx(49.0)
    assert calculate_ratio_score(7.0) == pytest.approx(55.3)
    assert calculate_ratio_score(10.0) == pytest.approx(63.0)
    assert calculate_ratio_score(20.0) == pytest.approx(70.0)
    assert calculate_ratio_score(100.0) == pytest.approx(70.0)


def test_grass_score_mission_component():
    """Verify mission completion contributes strictly 15 or 0 points."""
    assert calculate_mission_score(True) == 15.0
    assert calculate_mission_score(False) == 0.0


def test_grass_score_field_time_component():
    """Verify phone-free field time is bounded between 0 and 10 points across milestones."""
    durations = [0, 30, 60, 120, 300, 600, 1200]
    prev_pts = -1.0

    for d in durations:
        pts = calculate_field_time_score(d)
        assert 0.0 <= pts <= 10.0, f"Field time score {pts} out of bounds for duration {d}"
        assert pts >= prev_pts, f"Field time not monotonic at {d}: {pts} < {prev_pts}"
        prev_pts = pts

    assert calculate_field_time_score(0) == 0.0
    assert calculate_field_time_score(30) == 3.0
    assert calculate_field_time_score(60) == 5.0
    assert calculate_field_time_score(120) == 7.0
    assert calculate_field_time_score(300) == 8.5
    assert calculate_field_time_score(600) == 10.0
    assert calculate_field_time_score(1200) == 10.0


def test_grass_score_reflection_component():
    """Verify reflection scoring tiers: empty (0), short (2), meaningful (4), curiosity (5)."""
    # Empty
    assert calculate_reflection_score("") == 0.0
    assert calculate_reflection_score("   ") == 0.0
    assert calculate_reflection_score(None) == 0.0

    # Short (<15 chars)
    assert calculate_reflection_score("green leaf") == 2.0

    # Meaningful observation
    obs = "The underside of the foliage had distinct parallel veins with slight serration."
    assert calculate_reflection_score(obs) == 4.0

    # Meaningful observation + curiosity
    obs_curiosity = "The underside was lighter green. Why do the vein angles shift toward the tip?"
    assert calculate_reflection_score(obs_curiosity) == 5.0

    obs_wonder = "I noticed three distinct raised ribs and wonder how they transport sap."
    assert calculate_reflection_score(obs_wonder) == 5.0


def test_grass_score_final_bounds_and_determinism():
    """Verify 0 <= final_score <= 100 and determinism across runs."""
    # Worst case: 0 exploration
    res_zero = calculate_grass_score(
        screen_time_seconds=600,
        field_time_seconds=0,
        mission_completed=False,
        user_observation=""
    )
    assert 0 <= res_zero["score"] <= 100
    assert res_zero["breakdown"]["mission_points"] == 0
    assert res_zero["breakdown"]["field_time_points"] == 0
    assert res_zero["breakdown"]["reflection_points"] == 0

    # Best case: high ratio, completed, long time, curiosity
    res_max = calculate_grass_score(
        screen_time_seconds=10,
        field_time_seconds=1200,
        mission_completed=True,
        user_observation="Detailed observation of textures. How do these stomata regulate moisture?"
    )
    assert 0 <= res_max["score"] <= 100
    assert res_max["score"] == 100

    # Determinism: identical calls yield identical results
    run1 = calculate_grass_score(screen_time_seconds=38, field_time_seconds=261, mission_completed=True, user_observation="Test observation text.")
    run2 = calculate_grass_score(screen_time_seconds=38, field_time_seconds=261, mission_completed=True, user_observation="Test observation text.")
    assert run1 == run2


def test_grass_score_e2e_regression_not_100():
    """
    CRITICAL REGRESSION TEST:
    World Time = 261 sec, Screen Time = 38 sec, Ratio ≈ 6.87x,
    Mission = completed, Phone-free = 261 sec, Reflection = completed.
    The score MUST NOT automatically be 100. It must produce exactly 82 points.
    """
    res = calculate_grass_score(
        screen_time_seconds=38,
        field_time_seconds=261,
        phone_free_seconds=261,
        mission_completed=True,
        user_observation="The underside of the leaf was lighter green and had prominent raised veins."
    )

    # Must be bounded and realistic, NOT 100
    assert res["score"] < 100
    assert res["score"] == 82
    assert res["grass_score"] == 82

    # Verify breakdown components
    bd = res["breakdown"]
    assert bd["ratio_points"] == 55
    assert bd["mission_points"] == 15
    assert bd["field_time_points"] == 8
    assert bd["reflection_points"] == 4

    # Verify metrics
    met = res["metrics"]
    assert met["world_time_seconds"] == 261
    assert met["screen_time_seconds"] == 38
    assert met["world_screen_ratio"] == 6.87
    assert met["mission_completed"] is True
    assert met["phone_free_seconds"] == 261
    assert met["reflection_completed"] is True

    # Legacy fields
    assert "ratio" in res
    assert "ratio_formatted" in res
    assert "verdict" in res


def test_ollama_unavailable_fallback():
    async def run_check():
        generator = MissionGenerator(ai_provider=MockProvider())
        mission = await generator.generate_mission(
            object_name="Neem Leaf",
            category="leaf",
            confidence=0.74
        )
        assert mission is not None
        assert "instruction" in mission
        assert "safety_note" in mission

    asyncio.run(run_check())


def test_structured_reflection():
    async def run_check():
        generator = MissionGenerator(ai_provider=MockProvider())
        reflection = await generator.generate_reflection(
            object_name="Neem Leaf",
            category="leaf",
            mission_title="Underside Architecture",
            user_observation="The bottom was lighter green with raised parallel veins.",
            field_time_seconds=261
        )
        assert "reflection" in reflection
        assert "observation_highlight" in reflection
        assert "curiosity_fact" in reflection
        assert "next_suggestion" in reflection

    asyncio.run(run_check())


# ==========================================
# 6. End-to-End Pipeline Test
# ==========================================

def test_full_pipeline_image_to_journal():
    """
    Test full WildSense pipeline:
    image -> recognition -> session -> mission -> complete -> reflection -> grass score -> sqlite journal
    """
    # 1. Real image recognition via multipart upload
    img_bytes = create_test_image(color=(34, 139, 34))
    rec_res = client.post("/api/recognize", files={"image": ("specimen.png", img_bytes, "image/png")})
    assert rec_res.status_code == 200
    rec_data = rec_res.json()

    # 2. Initialize exploration session in SQLite
    sess_res = client.post("/api/sessions", json={
        "object_name": rec_data["common_name"],
        "category": rec_data["category"],
        "confidence": rec_data["confidence"],
        "description": rec_data["description"],
        "uncertainty": rec_data["uncertainty"]
    })
    assert sess_res.status_code == 200
    session_id = sess_res.json()["id"]

    # 3. Generate observation mission
    mis_res = client.post("/api/mission", json={
        "object_name": rec_data["common_name"],
        "category": rec_data["category"],
        "confidence": rec_data["confidence"],
        "session_id": session_id,
        "available_time_minutes": 2
    })
    assert mis_res.status_code == 200
    mission_data = mis_res.json()
    assert "instruction" in mission_data

    # 4. Field session complete & reflection
    comp_res = client.post(f"/api/sessions/{session_id}/complete", json={
        "screen_time_seconds": 25,
        "field_time_seconds": 180,
        "user_observation": "The foliage had parallel pinnate venation."
    })
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert comp_data["grass_score"]["grass_score"] >= 70
    assert "breakdown" in comp_data["grass_score"]
    assert "metrics" in comp_data["grass_score"]
    assert "reflection_details" in comp_data

    # 5. Verify SQLite Journal persistence
    journ_res = client.get("/api/journal")
    assert journ_res.status_code == 200
    entries = journ_res.json()
    assert len(entries) > 0
    latest = entries[0]
    assert latest["id"] == session_id
    assert latest["category"] == rec_data["category"]


# ==========================================
# 7. Model Selection & Gemma Integration Tests (Task 5)
# ==========================================

def test_model_selection_and_configuration():
    """Verify reasoning model selection works dynamically without restarting."""
    from services.ollama_provider import OllamaProvider
    provider = OllamaProvider(model="qwen3:4b")
    assert provider.model_name == "qwen3:4b"

    provider.set_model("gemma2:2b")
    assert provider.model_name == "gemma2:2b"


def test_api_models_endpoint():
    """Verify GET /api/models returns available models and current active model."""
    res = client.get("/api/models")
    assert res.status_code == 200
    data = res.json()
    assert "active_model" in data
    assert "available_models" in data
    assert "reasoning_provider" in data
    assert isinstance(data["available_models"], list)


def test_api_models_select_endpoint():
    """Verify POST /api/models/select dynamically switches reasoning model."""
    # Switch to gemma2:2b
    res = client.post("/api/models/select", json={"model": "gemma2:2b"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["active_model"] == "gemma2:2b"

    # Verify health endpoint reflects gemma2:2b
    health = client.get("/health").json()
    assert health["configured_model"] == "gemma2:2b"
    assert health["reasoning_model"] == "gemma2:2b"

    # Switch back to qwen3:4b
    res2 = client.post("/api/models/select", json={"model": "qwen3:4b"})
    assert res2.status_code == 200
    assert res2.json()["active_model"] == "qwen3:4b"

    health2 = client.get("/health").json()
    assert health2["configured_model"] == "qwen3:4b"
    assert health2["reasoning_model"] == "qwen3:4b"


def test_gemma_mission_generation_schema():
    """Verify Gemma produces valid 7-field structured schema and passes safety."""
    from services.ollama_provider import OllamaProvider
    gemma_provider = OllamaProvider(model="gemma2:2b")
    generator = MissionGenerator(ai_provider=gemma_provider)

    test_gemma_json = (
        '{"title": "Underside Architecture", '
        '"instruction": "Look underneath the leaf and compare the veins and texture with the upper surface.", '
        '"why": "The underside can reveal structures that are difficult to notice from above.", '
        '"estimated_minutes": 2, '
        '"physical_action": "Crouch slightly without touching the plant.", '
        '"observation_goal": "Find three differences.", '
        '"safety_note": "Observe without picking, tearing, or damaging the plant."}'
    )
    parsed = generator._parse_json_mission(test_gemma_json)
    assert parsed is not None
    assert "title" in parsed
    assert "instruction" in parsed
    assert "why" in parsed
    assert "estimated_minutes" in parsed
    assert "physical_action" in parsed
    assert "observation_goal" in parsed
    assert "safety_note" in parsed
    assert generator.validate_safety(parsed) is True


def test_unavailable_model_graceful_fallback():
    """Verify mission generation falls back gracefully when an unavailable model is configured."""
    from services.ollama_provider import OllamaProvider
    fake_provider = OllamaProvider(model="nonexistent_gemma_model_9999")
    generator = MissionGenerator(ai_provider=fake_provider)

    mission = asyncio.run(generator.generate_mission(
        object_name="Test Wild Plant",
        category="plant",
        confidence=0.65,
        available_time_minutes=2
    ))

    assert "title" in mission
    assert "instruction" in mission
    assert "why" in mission
    assert "estimated_minutes" in mission
    assert "physical_action" in mission
    assert "observation_goal" in mission
    assert "safety_note" in mission
    assert mission["provider"] in {"rule_strategy_fallback", "mock", "fallback"}
    assert generator.validate_safety(mission) is True


# ==========================================
# 8. Audio Provider & ElevenLabs Integration Tests (Task 6)
# ==========================================

import httpx
from unittest.mock import AsyncMock, patch
from services.audio_provider import (
    format_mission_narration,
    get_audio_provider,
    generate_audio_with_fallback,
    ElevenLabsAudioProvider,
    BrowserAudioProvider,
    MockAudioProvider,
    AudioMissionProvider,
)


def test_audio_provider_interface_and_defaults():
    """1. Audio provider configuration defaults and interface enforcement."""
    assert issubclass(BrowserAudioProvider, AudioMissionProvider)
    assert issubclass(MockAudioProvider, AudioMissionProvider)
    assert issubclass(ElevenLabsAudioProvider, AudioMissionProvider)

    # BrowserAudioProvider defaults
    browser = BrowserAudioProvider()
    assert browser.provider_name == "browser"
    res = asyncio.run(browser.generate_audio("Look closely at the leaf veins."))
    assert res["status"] == "ready"
    assert res["provider"] == "browser"
    assert res["supports_client_speech"] is True
    assert res["audio_url"] is None

    # ElevenLabsAudioProvider defaults
    eleven = ElevenLabsAudioProvider(api_key="mock_key", voice_id="mock_voice")
    assert eleven.provider_name == "elevenlabs"
    assert eleven.model_id == "eleven_flash_v2_5"
    assert eleven.timeout_seconds == 15.0
    assert eleven.is_configured() is True


def test_elevenlabs_request_construction():
    """2. Verify exact ElevenLabs HTTP request construction, URL, headers, and body."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    fake_mp3 = b"ID3\x03\x00\x00\x00\x00MOCK_MP3_PAYLOAD_BYTES"
    mock_response = httpx.Response(200, content=fake_mp3, headers={"content-type": "audio/mpeg"})
    mock_client.post.return_value = mock_response

    provider = ElevenLabsAudioProvider(
        api_key="test_secret_key_123",
        voice_id="EXAVITQu4vr4xnSDxMaL",
        model_id="eleven_flash_v2_5",
        timeout_seconds=12.0,
        http_client=mock_client
    )

    audio_bytes = asyncio.run(provider.synthesize_bytes("Observe the bark texture."))
    assert audio_bytes == fake_mp3

    # Inspect the exact call args made to httpx
    mock_client.post.assert_called_once()
    call_args, call_kwargs = mock_client.post.call_args

    # Check URL
    assert call_args[0] == "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

    # Check headers
    headers = call_kwargs["headers"]
    assert headers["xi-api-key"] == "test_secret_key_123"
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "audio/mpeg"

    # Check body payload
    payload = call_kwargs["json"]
    assert payload["text"] == "Observe the bark texture."
    assert payload["model_id"] == "eleven_flash_v2_5"
    assert "voice_settings" in payload
    assert payload["voice_settings"]["stability"] == 0.50
    assert payload["voice_settings"]["similarity_boost"] == 0.75
    assert call_kwargs["timeout"] == 12.0


def test_successful_mocked_audio_response():
    """3. Verify successful audio synthesis returns in-memory base64 data URI."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    fake_mp3 = b"MOCK_ELEVENLABS_MP3_STREAM"
    mock_client.post.return_value = httpx.Response(200, content=fake_mp3)

    provider = ElevenLabsAudioProvider(
        api_key="key",
        voice_id="voice123",
        http_client=mock_client
    )

    result = asyncio.run(provider.generate_audio("Notice the serrations on the leaf margins."))
    assert result["status"] == "ready"
    assert result["provider"] == "elevenlabs"
    assert result["supports_client_speech"] is False
    assert result["audio_url"].startswith("data:audio/mpeg;base64,")
    assert result["audio_base64"] is not None
    assert result["model"] == "eleven_flash_v2_5"
    assert result["duration_seconds"] > 0


def test_missing_api_key_or_voice():
    """4. Verify missing API key or voice ID fails gracefully."""
    p_no_key = ElevenLabsAudioProvider(api_key="", voice_id="voice123")
    assert p_no_key.is_configured() is False
    with pytest.raises(ValueError, match="API key is not configured"):
        asyncio.run(p_no_key.synthesize_bytes("Test text"))

    p_no_voice = ElevenLabsAudioProvider(api_key="key123", voice_id="")
    assert p_no_voice.is_configured() is False
    with pytest.raises(ValueError, match="voice ID is not configured"):
        asyncio.run(p_no_voice.synthesize_bytes("Test text"))


def test_invalid_voice_configuration_or_provider_error():
    """5. Verify HTTP 404 (voice not found) or upstream errors are handled cleanly."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = httpx.Response(404, text='{"detail":"Voice not found"}')

    provider = ElevenLabsAudioProvider(
        api_key="key",
        voice_id="invalid_voice_id",
        http_client=mock_client
    )

    with pytest.raises(ValueError, match="not found"):
        asyncio.run(provider.synthesize_bytes("Test text"))


def test_timeout_and_rate_limit_handling():
    """6. Verify timeout (TimeoutError), rate limits (429), and auth failure (401)."""
    # 6a. Timeout
    timeout_client = AsyncMock(spec=httpx.AsyncClient)
    timeout_client.post.side_effect = httpx.TimeoutException("Connection timed out")
    p_timeout = ElevenLabsAudioProvider(api_key="key", voice_id="v", http_client=timeout_client)
    with pytest.raises(TimeoutError, match="timed out"):
        asyncio.run(p_timeout.synthesize_bytes("Test text"))

    # 6b. Rate limit (429)
    rate_client = AsyncMock(spec=httpx.AsyncClient)
    rate_client.post.return_value = httpx.Response(429, text="Quota exceeded")
    p_rate = ElevenLabsAudioProvider(api_key="key", voice_id="v", http_client=rate_client)
    with pytest.raises(RuntimeError, match="rate limit or quota exceeded"):
        asyncio.run(p_rate.synthesize_bytes("Test text"))

    # 6c. Auth failure (401)
    auth_client = AsyncMock(spec=httpx.AsyncClient)
    auth_client.post.return_value = httpx.Response(401, text="Unauthorized")
    p_auth = ElevenLabsAudioProvider(api_key="bad_key", voice_id="v", http_client=auth_client)
    with pytest.raises(PermissionError, match="authentication failed"):
        asyncio.run(p_auth.synthesize_bytes("Test text"))


def test_safe_browser_speech_fallback():
    """7. Safe browser-speech fallback when ElevenLabs is unconfigured or encounters errors."""
    # When ElevenLabs is unconfigured, fallback must succeed seamlessly
    with patch("services.audio_provider.ELEVENLABS_API_KEY", ""):
        result = asyncio.run(generate_audio_with_fallback(
            text="Observe the moss on the bark.",
            preferred_provider="elevenlabs"
        ))
        assert result["status"] == "fallback"
        assert result["provider"] == "browser"
        assert result["supports_client_speech"] is True
        assert "not configured" in result["fallback_reason"].lower()

    # When user explicitly selects browser speech, ElevenLabs is NEVER called
    result_browser = asyncio.run(generate_audio_with_fallback(
        text="Observe the moss on the bark.",
        preferred_provider="browser"
    ))
    assert result_browser["status"] == "ready"
    assert result_browser["provider"] == "browser"
    assert result_browser["supports_client_speech"] is True


def test_correct_response_content_type_and_endpoints():
    """8. Test /api/audio JSON response and /api/audio/status endpoint."""
    # Test /api/audio/status
    res_status = client.get("/api/audio/status")
    assert res_status.status_code == 200
    st_data = res_status.json()
    assert "configured_provider" in st_data
    assert "browser_speech_supported" in st_data
    assert "model_id" in st_data
    # Verify no secret keys leaked in status endpoint
    assert "api_key" not in st_data
    assert "sk_" not in str(st_data)

    # Test POST /api/audio with valid mission fields
    res_audio = client.post("/api/audio", json={
        "title": "Underside Architecture",
        "instruction": "Look underneath the leaf and compare the veins.",
        "physical_action": "Crouch slightly without touching the plant.",
        "observation_goal": "Find three differences in texture.",
        "safety_note": "Observe without picking or tearing foliage.",
        "estimated_minutes": 2,
        "provider": "browser"
    })
    assert res_audio.status_code == 200
    audio_data = res_audio.json()
    assert audio_data["provider"] == "browser"
    assert "Underside Architecture" in audio_data["text"]
    assert audio_data["duration_seconds"] > 0
    assert audio_data["supports_client_speech"] is True


def test_concise_narration_formatting():
    """9. Test concise narration formatting converts mission into spoken instructions."""
    raw_mission = {
        "title": "**Underside Architecture**",
        "instruction": "Don't pick the leaf. Look underneath it and compare the veins, texture, and color.",
        "why": "Vascular structures are hidden from above.",
        "estimated_minutes": 2,
        "physical_action": "Crouch slightly and gently tilt your perspective.",
        "observation_goal": "Find three differences between top and bottom surfaces.",
        "safety_note": "Observe without damaging or removing the foliage."
    }

    narration = format_mission_narration(raw_mission)

    # Must contain essential spoken guide components
    assert "Underside Architecture" in narration
    assert "2-minute" in narration
    assert "Look underneath it" in narration
    assert "Crouch slightly" in narration
    assert "Observation goal:" in narration
    assert "Safety note:" in narration

    # Must strip markdown formatting
    assert "**" not in narration
    assert "#" not in narration

    # Must be concise (~15-35 seconds spoken time, ~35-70 words)
    words = narration.split()
    assert 25 <= len(words) <= 75, f"Narration word count unexpected: {len(words)}"


def test_privacy_and_data_isolation_verification():
    """10. Verify no user images, reflections, or private credentials are sent or leaked."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = httpx.Response(200, content=b"AUDIO_BYTES")

    provider = ElevenLabsAudioProvider(
        api_key="sk_test_secret_private_key_value",
        voice_id="test_voice",
        http_client=mock_client
    )

    asyncio.run(provider.generate_audio("Look at the pattern on the trunk."))

    call_args, call_kwargs = mock_client.post.call_args
    sent_payload = call_kwargs["json"]

    # Verify ONLY text and synthesis parameters are sent to external API
    assert set(sent_payload.keys()) == {"text", "model_id", "voice_settings"}
    assert "image" not in sent_payload
    assert "image_url" not in sent_payload
    assert "journal" not in sent_payload
    assert "reflection" not in sent_payload
    assert "location" not in sent_payload

    # Verify secret key is not in JSON payload body
    assert "sk_test_secret_private_key_value" not in str(sent_payload)


def test_audio_endpoint_safety_enforcement():
    """11. Verify /api/audio rejects unsafe text and prevents bypassing safety validation."""
    # Attempting to narrate dangerous tasks must be rejected with 400
    dangerous_requests = [
        {"text": "Taste the wild berry to see if it is sweet.", "provider": "browser"},
        {"text": "Pick the leaf and rip it off the branch.", "provider": "browser"},
        {"text": "Touch unknown fungus with bare hands.", "provider": "browser"},
        {"text": "Approach the active bird nest and examine eggs.", "provider": "browser"}
    ]

    for req in dangerous_requests:
        res = client.post("/api/audio", json=req)
        assert res.status_code == 400
        assert "safety" in res.json()["detail"].lower()

    # Excessively long text rejected with 400
    long_res = client.post("/api/audio", json={"text": "x" * 2500, "provider": "browser"})
    assert long_res.status_code == 422 or long_res.status_code == 400


