import io
import sys
import time
from pathlib import Path
from PIL import Image
import httpx

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

def create_sample_specimen_image() -> bytes:
    """Generate in-memory specimen image for genuine CV analysis."""
    buf = io.BytesIO()
    # Green-dominant specimen image
    img = Image.new("RGB", (200, 200), color=(34, 150, 45))
    img.save(buf, format="PNG")
    return buf.getvalue()

def get_client():
    """Return live HTTP client if server is up, else FastAPI TestClient."""
    try:
        res = httpx.get("http://127.0.0.1:8000/health", timeout=1.5)
        if res.status_code == 200:
            print("Connected to live WildSense server at http://127.0.0.1:8000")
            return httpx.Client(base_url="http://127.0.0.1:8000", timeout=60.0)
    except Exception:
        pass

    print("Live server not detected at 127.0.0.1:8000. Using in-process ASGI test client.")
    from main import app
    from fastapi.testclient import TestClient
    return TestClient(app)

def test_task3_pipeline():
    client = get_client()

    print("\n================ WILDSENSE TASK 3 E2E PIPELINE ================")

    # 1. Health check
    health_res = client.get("/health")
    assert health_res.status_code == 200
    health = health_res.json()
    print("1. Health Status:")
    print(f"   Status: {health['status']}")
    print(f"   Ollama Connected: {health['ollama_connected']}")
    print(f"   Configured Reasoning Model: {health['configured_model']}")
    print(f"   Configured Vision Model: {health['vision_model']}")
    print(f"   Vision Available: {health['vision_available']}")
    assert health["status"] == "healthy"

    # 2. Vision Availability check
    vision_status_msg = "Real Vision Model Online" if health["vision_available"] else "Using Local CV In-Memory Heuristic Fallback"
    print(f"2. Vision Architecture Status: {vision_status_msg}")

    # 3. Real Image Recognition (Multipart Upload)
    sample_img_bytes = create_sample_specimen_image()
    files = {"image": ("field_specimen.png", sample_img_bytes, "image/png")}
    rec_res = client.post("/api/recognize", files=files)
    assert rec_res.status_code == 200
    rec = rec_res.json()
    print(f"3. Real Image Recognition Result:")
    print(f"   Category: {rec['category']}")
    print(f"   Common Name: {rec['common_name']}")
    print(f"   Confidence: {int(rec['confidence']*100)}%")
    print(f"   Uncertainty: {rec['uncertainty']}")
    print(f"   Inference Time: {rec.get('inference_ms', 0)}ms")
    print(f"   Provider: {rec['provider']}")
    assert rec["category"] in ["leaf", "plant", "flower", "tree", "rock", "other"]
    assert 0.0 <= rec["confidence"] <= 1.0

    # 4. Demo Recognition (Verify Presets still work)
    demo_res = client.post("/api/recognize", json={"preset_id": "demo_leaf"})
    assert demo_res.status_code == 200
    demo_rec = demo_res.json()
    print(f"4. Demo Preset Recognition: '{demo_rec['common_name']}' ({demo_rec['confidence']*100}%)")
    assert "Likely Neem" in demo_rec["common_name"]

    # 5. Initialize Exploration Session
    sess_res = client.post("/api/sessions", json={
        "object_name": rec["common_name"],
        "category": rec["category"],
        "confidence": rec["confidence"],
        "uncertainty": rec["uncertainty"],
        "description": rec["description"]
    })
    assert sess_res.status_code == 200
    session_id = sess_res.json()["id"]
    print(f"5. Session Initialized in SQLite. ID: {session_id}")

    # 6. Generate Contextual Observation Mission
    mission_res = client.post("/api/mission", json={
        "object_name": rec["common_name"],
        "category": rec["category"],
        "confidence": rec["confidence"],
        "session_id": session_id,
        "available_time_minutes": 2
    })
    assert mission_res.status_code == 200
    mission = mission_res.json()
    print("6. Contextual Mission Generated:")
    print(f"   Title: {mission['title']}")
    print(f"   Instruction: {mission['instruction']}")
    print(f"   Physical Action: {mission['physical_action']}")
    print(f"   Observation Goal: {mission['observation_goal']}")
    print(f"   Safety Note: {mission['safety_note']}")
    print(f"   LLM Inference: {mission.get('llm_inference_ms', 0)}ms (Provider: {mission.get('provider')})")
    assert "title" in mission
    assert "instruction" in mission
    assert "safety_note" in mission

    # 7. Audio Narration (Task 6: ElevenLabs & Browser Speech)
    # 7a. Audio Provider Status check
    audio_status_res = client.get("/api/audio/status")
    assert audio_status_res.status_code == 200
    audio_status = audio_status_res.json()
    print(f"7. Audio System Status:")
    print(f"   Default Provider: {audio_status['configured_provider']}")
    print(f"   ElevenLabs Configured: {audio_status['elevenlabs_configured']}")
    print(f"   Browser Speech Supported: {audio_status['browser_speech_supported']}")

    # 7b. Test explicit offline Browser Speech branch
    browser_audio_res = client.post("/api/audio", json={
        "title": mission["title"],
        "instruction": mission["instruction"],
        "physical_action": mission.get("physical_action", ""),
        "observation_goal": mission.get("observation_goal", ""),
        "safety_note": mission.get("safety_note", ""),
        "estimated_minutes": mission.get("estimated_minutes", 2),
        "provider": "browser"
    })
    assert browser_audio_res.status_code == 200
    browser_audio = browser_audio_res.json()
    print(f"   [Browser Branch] Provider={browser_audio['provider']}, Supports WebSpeech={browser_audio['supports_client_speech']}")
    assert browser_audio["provider"] == "browser"
    assert browser_audio["supports_client_speech"] is True

    # 7c. Test ElevenLabs branch (or safe fallback when unconfigured/offline)
    eleven_audio_res = client.post("/api/audio", json={
        "title": mission["title"],
        "instruction": mission["instruction"],
        "physical_action": mission.get("physical_action", ""),
        "observation_goal": mission.get("observation_goal", ""),
        "safety_note": mission.get("safety_note", ""),
        "estimated_minutes": mission.get("estimated_minutes", 2),
        "provider": "elevenlabs"
    })
    assert eleven_audio_res.status_code == 200
    eleven_audio = eleven_audio_res.json()
    if eleven_audio["provider"] == "elevenlabs":
        print(f"   [ElevenLabs Branch] Genuine ElevenLabs audio generated successfully!")
        print(f"   Model: {eleven_audio.get('model')}, Voice: {eleven_audio.get('voice_id')}")
        print(f"   Data URL: {eleven_audio.get('audio_url', '')[:35]}... ({len(eleven_audio.get('audio_url', ''))} chars)")
        assert eleven_audio["status"] == "ready"
        assert eleven_audio["audio_url"] is not None
        assert eleven_audio["audio_url"].startswith("data:audio/mpeg;base64,")
    else:
        print(f"   [ElevenLabs Branch] Safe fallback active: {eleven_audio.get('fallback_reason')}")
        assert eleven_audio["status"] == "fallback"
        assert eleven_audio["provider"] == "browser"
        assert eleven_audio["supports_client_speech"] is True


    # 8. Field Session Completion & Grass Score (Task 4 Regression Test)
    comp_res = client.post(f"/api/sessions/{session_id}/complete", json={
        "screen_time_seconds": 38,
        "field_time_seconds": 261,
        "user_observation": "The specimen foliage displayed distinct alternating venation."
    })
    assert comp_res.status_code == 200
    comp = comp_res.json()
    score = comp["grass_score"]
    reflection = comp["reflection_details"]
    breakdown = score.get("breakdown", {})
    metrics = score.get("metrics", {})

    print("8. Field Session Concluded & Explainable Grass Score Breakdown:")
    print(f"   SCREEN TIME: {score['screen_time_formatted']}")
    print(f"   FIELD TIME: {score['field_time_formatted']}")
    print(f"   WORLD / SCREEN RATIO: {score['ratio_formatted']}")
    print(f"   GRASS SCORE: {score['score']} / 100 ({score['verdict']})")
    print("   SCORE BREAKDOWN:")
    print(f"     🌿 World / Screen Ratio: {breakdown.get('ratio_points')} / 70")
    print(f"     ✓ Mission Completed:     {breakdown.get('mission_points')} / 15")
    print(f"     📵 Phone-Free Time:       {breakdown.get('field_time_points')} / 10")
    print(f"     💭 Reflection:            {breakdown.get('reflection_points')} / 5")
    print(f"     TOTAL:                   {score['score']} / 100")
    print(f"   Human Explanation: \"{score.get('explanation')}\"")
    print(f"   AI Reflection: \"{reflection['reflection']}\"")
    print(f"   Curiosity Fact: \"{reflection['curiosity_fact']}\"")
    print(f"   Next Suggestion: \"{reflection['next_suggestion']}\"")

    # Critical Task 4 Regression Check: 6.87x MUST NOT be 100!
    assert score["score"] < 100, f"Expected score < 100, got {score['score']}"
    assert score["score"] == 82, f"Expected exact score 82, got {score['score']}"
    assert breakdown.get("ratio_points") == 55
    assert breakdown.get("mission_points") == 15
    assert breakdown.get("field_time_points") == 8
    assert breakdown.get("reflection_points") == 4

    # 9. Verify SQLite Journal Entry
    journal_res = client.get("/api/journal")
    assert journal_res.status_code == 200
    journal = journal_res.json()
    print(f"9. SQLite Journal Entries Count: {len(journal)}")
    latest = journal[0]
    assert latest["id"] == session_id
    assert latest["mission_title"] == mission["title"]
    assert latest["grass_score"] == score["score"]

    print("\n✓ SUCCESS: All 9 pipeline steps passed successfully!")
    print("================================================================\n")

if __name__ == "__main__":
    test_task3_pipeline()
