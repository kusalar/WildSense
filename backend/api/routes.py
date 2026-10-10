from typing import Optional, List, Dict, Any
import io
import time
from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, File, Form, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from PIL import Image
from database import get_db
from config import (
    DEFAULT_MODEL,
    REASONING_MODEL,
    GEMMA_MODEL,
    OLLAMA_BASE_URL,
    VISION_MODEL,
    AUDIO_PROVIDER,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    ELEVENLABS_MODEL_ID,
)
from services.ollama_provider import OllamaProvider
from services.ai_provider import MockProvider
from services.recognizer import ObjectRecognizer
from services.mission_generator import MissionGenerator
from services.grass_score import calculate_grass_score
from services.journal import JournalService
from services.audio_provider import (
    format_mission_narration,
    get_audio_provider,
    generate_audio_with_fallback,
    ElevenLabsAudioProvider,
    BrowserAudioProvider,
    MockAudioProvider
)
from services.plant_service import PlantService

router = APIRouter()



# Instantiate core singletons
ollama_provider = OllamaProvider(base_url=OLLAMA_BASE_URL, model=REASONING_MODEL)
mock_provider = MockProvider()
recognizer = ObjectRecognizer()
mission_generator = MissionGenerator(ai_provider=ollama_provider)
audio_provider = MockAudioProvider()

MAX_IMAGE_BYTES = 15 * 1024 * 1024  # 15MB limit
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}


# --- Request/Response Schemas ---
class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    configured_model: str
    reasoning_model: str
    vision_model: str
    vision_available: bool
    available_models: List[str]
    mode: str
    onnx_available: bool = False
    onnx_model: Optional[str] = None
    specialist_available: bool = False
    specialist_enabled: bool = False

class ModelSelectRequest(BaseModel):
    model: str

class RecognizeRequest(BaseModel):
    image_base64: Optional[str] = None
    images_base64: Optional[List[str]] = None
    preset_id: Optional[str] = None
    organ_type: Optional[str] = "whole_plant"

class RecognizeResponse(BaseModel):
    category: str
    common_name: str
    confidence: float
    description: str
    uncertainty: str
    inference_ms: int = 0
    provider: str = "local"
    scientific_name: Optional[str] = None
    similarity_score: Optional[float] = None
    raw_cosine: Optional[float] = None
    organ_type: Optional[str] = None
    organ_tip: Optional[str] = None
    match_level: Optional[str] = None
    match_details: Optional[str] = None
    photos_count: int = 1
    aggregation: Optional[str] = None
    individual_photos: Optional[List[Dict[str, Any]]] = None
    candidates: Optional[List[Dict[str, Any]]] = None
    image_quality: Optional[Dict[str, Any]] = None
    arbitration: Optional[Dict[str, Any]] = None


class MissionRequest(BaseModel):
    object_name: str
    category: str
    confidence: float = 0.74
    difficulty: str = "normal"
    available_time_minutes: int = 2
    context: Optional[str] = None
    session_id: Optional[str] = None
    description: Optional[str] = None
    uncertainty: Optional[str] = None

class MissionResponse(BaseModel):
    title: str
    instruction: str
    why: str
    estimated_minutes: int
    physical_action: str
    observation_goal: str
    safety_note: str
    llm_inference_ms: Optional[int] = None
    provider: Optional[str] = None
    model: Optional[str] = None

class SessionCreateRequest(BaseModel):
    object_name: str
    category: str
    confidence: float = 0.74
    description: Optional[str] = None
    uncertainty: Optional[str] = None
    image_url: Optional[str] = None

class SessionCompleteRequest(BaseModel):
    screen_time_seconds: int
    field_time_seconds: int
    user_observation: Optional[str] = None

class ReflectionResponse(BaseModel):
    reflection: str
    observation_highlight: str
    curiosity_fact: str
    next_suggestion: str

class ReflectionRequest(BaseModel):
    object_name: str
    category: str
    mission_title: str
    user_observation: str
    field_time_seconds: int

class AudioRequest(BaseModel):
    text: Optional[str] = Field(None, max_length=2000, description="Optional raw narration text")
    title: Optional[str] = Field(None, max_length=200, description="Mission title")
    instruction: Optional[str] = Field(None, max_length=600, description="Mission core instruction")
    physical_action: Optional[str] = Field(None, max_length=400, description="Physical movement task")
    observation_goal: Optional[str] = Field(None, max_length=400, description="Specific visual detail to observe")
    safety_note: Optional[str] = Field(None, max_length=400, description="Essential safety instruction")
    estimated_minutes: Optional[int] = Field(None, ge=1, le=60, description="Mission duration in minutes")
    provider: Optional[str] = Field(None, description="Preferred audio provider ('browser' or 'elevenlabs')")

class AudioResponse(BaseModel):
    status: str
    provider: str
    text: str
    duration_seconds: float
    supports_client_speech: bool
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    speech_rate: float = 1.0
    pitch: float = 1.0
    voice_id: Optional[str] = None
    model: Optional[str] = None
    fallback_reason: Optional[str] = None

class ScoreBreakdown(BaseModel):

    ratio_points: int
    mission_points: int
    field_time_points: int
    reflection_points: int
    max_ratio_points: int = 70
    max_mission_points: int = 15
    max_field_time_points: int = 10
    max_reflection_points: int = 5
    raw_ratio_points: Optional[float] = None
    raw_field_time_points: Optional[float] = None

class ScoreMetrics(BaseModel):
    world_time_seconds: int
    screen_time_seconds: int
    world_screen_ratio: float
    mission_completed: bool
    phone_free_seconds: int
    reflection_completed: bool

class GrassScoreResponse(BaseModel):
    score: int
    grass_score: int
    breakdown: ScoreBreakdown
    metrics: ScoreMetrics
    screen_time_seconds: int
    field_time_seconds: int
    screen_time_formatted: str
    field_time_formatted: str
    ratio: float
    ratio_formatted: str
    verdict: str
    explanation: Optional[str] = None


# --- Endpoints ---
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Verify backend status, Ollama daemon reachability, and vision model status."""
    is_connected = await ollama_provider.is_available()
    available_models = []
    vision_available = False

    onnx_available = await recognizer.is_onnx_available()
    if is_connected:
        available_models = await ollama_provider.list_models()
        if available_models and ollama_provider.model_name not in available_models:
            ollama_provider.set_model(available_models[0])
        vision_available = await recognizer.is_vision_available()
    else:
        vision_available = onnx_available

    return HealthResponse(
        status="healthy",
        ollama_connected=is_connected,
        configured_model=ollama_provider.model_name,
        reasoning_model=ollama_provider.model_name,
        vision_model=VISION_MODEL,
        vision_available=vision_available,
        available_models=available_models,
        mode="local_ollama" if is_connected else "fallback_mock",
        onnx_available=onnx_available,
        onnx_model="BioCLIP-FastViT-4271 (fp32 ONNX)" if onnx_available else None,
        specialist_available=recognizer.onnx_botany.specialist_available,
        specialist_enabled=recognizer.onnx_botany.specialist_enabled
    )


@router.get("/models")
async def get_models():
    """List available reasoning models and show active model."""
    is_connected = await ollama_provider.is_available()
    models = await ollama_provider.list_models() if is_connected else []
    return {
        "active_model": ollama_provider.model_name,
        "reasoning_model": ollama_provider.model_name,
        "available_models": models,
        "default_model": DEFAULT_MODEL,
        "gemma_model": GEMMA_MODEL,
        "reasoning_provider": "ollama" if is_connected else "mock"
    }

@router.post("/models/select")
async def select_model(req: ModelSelectRequest):
    """Switch active reasoning model between local models (e.g. gemma2:2b and qwen3:4b)."""
    ollama_provider.set_model(req.model)
    return {
        "status": "success",
        "active_model": ollama_provider.model_name,
        "provider": "ollama"
    }

@router.get("/presets")
async def get_presets():
    """Return all built-in demo observation presets for evaluation."""
    return recognizer.get_presets()

@router.post("/recognize", response_model=RecognizeResponse)
async def recognize_object(request: Request):
    """
    Unified recognition endpoint supporting:
    1. Multipart/form-data with image upload (real local CV/vision pipeline)
    2. JSON payload with image_base64 or preset_id (demo presets & backwards compatibility)
    """
    content_type = request.headers.get("content-type", "")

    # 1. Handle multipart/form-data file upload
    if "multipart/form-data" in content_type:
        form = await request.form()
        preset_id = form.get("preset_id")
        organ_type = form.get("organ_type") or "whole_plant"

        if preset_id and str(preset_id).strip():
            result = await recognizer.recognize(preset_id=str(preset_id), organ_type=str(organ_type))
            return RecognizeResponse(**result)

        # Retrieve file list: support 'images' list or fallback to single 'image'
        files = form.getlist("images")
        if not files:
            single = form.get("image")
            if single:
                files = [single]

        if not files:
            raise HTTPException(status_code=400, detail="Missing 'image' or 'images' in multipart upload")

        if len(files) > 3:
            raise HTTPException(status_code=400, detail="Maximum 3 specimen photos allowed per observation")

        images_bytes = []
        for file_obj in files:
            if not hasattr(file_obj, "read"):
                continue
            if hasattr(file_obj, "content_type") and file_obj.content_type:
                mime = file_obj.content_type.lower()
                if mime not in ALLOWED_MIME_TYPES and mime not in {"application/octet-stream", "image/jpg"}:
                    raise HTTPException(status_code=400, detail=f"Unsupported MIME type: {mime}. Allowed: image/jpeg, image/png, image/webp")

            b = await file_obj.read()
            if len(b) == 0:
                raise HTTPException(status_code=400, detail="Uploaded image file is empty")
            if len(b) > MAX_IMAGE_BYTES:
                raise HTTPException(status_code=400, detail="Image exceeds 15MB size limit")

            try:
                with Image.open(io.BytesIO(b)) as img:
                    fmt = img.format.upper() if img.format else ""
                    if fmt not in {"JPEG", "PNG", "WEBP"}:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Unsupported image format: {fmt or 'unknown'}. Allowed formats: image/jpeg, image/png, image/webp"
                        )
                    img.verify()
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid or malformed image format")

            images_bytes.append(b)

        result = await recognizer.recognize_multi_bytes(images_bytes, organ_type=str(organ_type))
        return RecognizeResponse(**result)

    # 2. Handle JSON payload
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request body format")

    preset_id = body.get("preset_id")
    image_base64 = body.get("image_base64")
    images_base64 = body.get("images_base64")
    organ_type = body.get("organ_type") or "whole_plant"

    if not preset_id and not image_base64 and not images_base64:
        raise HTTPException(status_code=400, detail="Provide either 'preset_id', 'image_base64', or 'images_base64'")

    if preset_id:
        result = await recognizer.recognize(preset_id=str(preset_id), organ_type=str(organ_type))
        return RecognizeResponse(**result)

    # Collect list of base64 inputs (up to 3)
    raw_list = []
    if images_base64 and isinstance(images_base64, list):
        raw_list = images_base64
    elif image_base64:
        raw_list = [image_base64]

    if len(raw_list) > 3:
        raise HTTPException(status_code=400, detail="Maximum 3 specimen photos allowed per observation")

    import base64
    import re
    decoded_bytes = []
    for raw_item in raw_list:
        try:
            raw_b64 = re.sub(r"^data:image/[a-zA-Z0-9\+\-\.]+;base64,", "", str(raw_item).strip())
            b64_bytes = base64.b64decode(raw_b64)
            if len(b64_bytes) == 0:
                raise HTTPException(status_code=400, detail="Provided image data is empty")
            if len(b64_bytes) > MAX_IMAGE_BYTES:
                raise HTTPException(status_code=400, detail="Image exceeds 15MB size limit")
            with Image.open(io.BytesIO(b64_bytes)) as img:
                fmt = img.format.upper() if img.format else ""
                if fmt not in {"JPEG", "PNG", "WEBP"}:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported image format: {fmt or 'unknown'}. Allowed formats: JPEG, PNG, WebP"
                    )
                img.verify()
            decoded_bytes.append(b64_bytes)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or malformed base64 image data")

    result = await recognizer.recognize_multi_bytes(decoded_bytes, organ_type=str(organ_type))
    return RecognizeResponse(**result)


@router.post("/mission", response_model=MissionResponse)
async def generate_mission(req: MissionRequest, db: Session = Depends(get_db)):
    """Generate a real-world physical observation mission using local AI and category strategies."""
    mission = await mission_generator.generate_mission(
        object_name=req.object_name,
        category=req.category,
        confidence=req.confidence,
        difficulty=req.difficulty,
        available_time_minutes=req.available_time_minutes,
        context=req.context,
        description=req.description,
        uncertainty=req.uncertainty
    )

    if req.session_id:
        JournalService.update_mission(
            db=db,
            session_id=req.session_id,
            mission_title=mission["title"],
            mission_instruction=mission["instruction"],
            estimated_minutes=mission["estimated_minutes"],
            physical_action=mission["physical_action"],
            safety_note=mission["safety_note"],
            mission_why=mission.get("why"),
            observation_goal=mission.get("observation_goal")
        )

    return MissionResponse(**mission)

@router.get("/audio/status")
async def get_audio_status():
    """Return non-sensitive audio provider configuration and readiness."""
    is_elevenlabs_ready = bool(ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID)
    return {
        "configured_provider": AUDIO_PROVIDER,
        "active_provider": "elevenlabs" if is_elevenlabs_ready and AUDIO_PROVIDER == "elevenlabs" else "browser",
        "elevenlabs_configured": is_elevenlabs_ready,
        "voice_id": ELEVENLABS_VOICE_ID if ELEVENLABS_VOICE_ID else None,
        "model_id": ELEVENLABS_MODEL_ID,
        "browser_speech_supported": True,
        "mode": "hybrid_optional_cloud" if is_elevenlabs_ready else "local_browser_speech"
    }

@router.post("/audio", response_model=AudioResponse)
async def generate_mission_audio(req: AudioRequest):
    """
    Audio-ready interface for field mode narration (Browser Web Speech & ElevenLabs).
    Ensures length validation, safety checks, and seamless offline-first fallback.
    """
    # 1. Resolve spoken text
    if req.text and req.text.strip():
        spoken_text = req.text.strip()
    elif req.title or req.instruction:
        spoken_text = format_mission_narration({
            "title": req.title or "",
            "instruction": req.instruction or "",
            "physical_action": req.physical_action or "",
            "observation_goal": req.observation_goal or "",
            "safety_note": req.safety_note or "",
            "estimated_minutes": req.estimated_minutes
        })
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'text' or structured mission fields ('title', 'instruction')"
        )

    # 2. Text validation and length limit
    if len(spoken_text) > 1500:
        raise HTTPException(
            status_code=400,
            detail="Narration text exceeds 1500 characters limit"
        )

    # 3. Deterministic safety validation (never bypass mission safety)
    if req.instruction or req.title:
        is_safe = mission_generator.validate_safety({
            "title": req.title or "Observation Mission",
            "instruction": req.instruction or "",
            "physical_action": req.physical_action or ""
        })
    else:
        is_safe = mission_generator.validate_safety({
            "title": "Observation Mission",
            "instruction": spoken_text
        })

    if not is_safe:
        raise HTTPException(
            status_code=400,
            detail="Audio narration text violates WildSense nature safety guidelines."
        )


    # 4. Generate audio with safe fallback
    audio_info = await generate_audio_with_fallback(
        text=spoken_text,
        preferred_provider=req.provider
    )
    return AudioResponse(**audio_info)

@router.post("/audio/raw")
async def generate_raw_mission_audio(req: AudioRequest):
    """
    Returns in-memory raw binary audio bytes (audio/mpeg) via ElevenLabs.
    Does not persist to disk. If ElevenLabs is unconfigured or fails, returns 503.
    """
    if req.text and req.text.strip():
        spoken_text = req.text.strip()
    elif req.title or req.instruction:
        spoken_text = format_mission_narration({
            "title": req.title or "",
            "instruction": req.instruction or "",
            "physical_action": req.physical_action or "",
            "observation_goal": req.observation_goal or "",
            "safety_note": req.safety_note or "",
            "estimated_minutes": req.estimated_minutes
        })
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'text' or structured mission fields ('title', 'instruction')"
        )

    if len(spoken_text) > 1500:
        raise HTTPException(status_code=400, detail="Narration text exceeds 1500 characters limit")

    if req.instruction or req.title:
        is_safe = mission_generator.validate_safety({
            "title": req.title or "Observation Mission",
            "instruction": req.instruction or "",
            "physical_action": req.physical_action or ""
        })
    else:
        is_safe = mission_generator.validate_safety({
            "title": "Observation Mission",
            "instruction": spoken_text
        })

    if not is_safe:
        raise HTTPException(status_code=400, detail="Audio narration text violates safety guidelines.")


    eleven = ElevenLabsAudioProvider()
    if not eleven.is_configured():
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs is not configured (missing API key or voice ID). Use /api/audio for browser speech."
        )

    try:
        audio_bytes = await eleven.synthesize_bytes(spoken_text)
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=mission.mp3"}
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"ElevenLabs audio synthesis failed: {str(exc)}"
        )


@router.post("/sessions")
async def create_session(req: SessionCreateRequest, db: Session = Depends(get_db)):
    """Initialize a new exploration session."""
    session_rec = JournalService.create_session(
        db=db,
        object_name=req.object_name,
        category=req.category,
        confidence=req.confidence,
        description=req.description,
        uncertainty=req.uncertainty,
        image_url=req.image_url
    )
    return {
        "id": session_rec.id,
        "status": session_rec.status,
        "created_at": session_rec.created_at.isoformat()
    }

@router.post("/sessions/{session_id}/complete")
async def complete_session(
    session_id: str,
    req: SessionCompleteRequest,
    db: Session = Depends(get_db)
):
    """Complete a session, calculate Grass Score, and create an AI reflection."""
    from models import SessionRecord
    record = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Session not found")

    reflection_data = await mission_generator.generate_reflection(
        object_name=str(record.object_name or ""),
        category=str(record.category or ""),
        mission_title=str(record.mission_title or "Nature Investigation"),
        user_observation=req.user_observation or "",
        field_time_seconds=req.field_time_seconds
    )

    completed = JournalService.complete_session(
        db=db,
        session_id=session_id,
        screen_time_seconds=req.screen_time_seconds,
        field_time_seconds=req.field_time_seconds,
        user_observation=req.user_observation,
        ai_reflection=reflection_data.get("reflection"),
        curiosity_fact=reflection_data.get("curiosity_fact"),
        next_suggestion=reflection_data.get("next_suggestion")
    )

    if not completed:
        raise HTTPException(status_code=404, detail="Session not found or failed to complete")

    score_metrics = calculate_grass_score(
        screen_time_seconds=req.screen_time_seconds,
        field_time_seconds=req.field_time_seconds,
        user_observation=req.user_observation,
        is_completed=True
    )

    completed_at_str = completed.completed_at.isoformat() if completed.completed_at else None

    return {
        "id": completed.id,
        "score": score_metrics["score"],
        "grass_score": score_metrics,
        "breakdown": score_metrics["breakdown"],
        "metrics": score_metrics["metrics"],
        "reflection_details": reflection_data,
        "ai_reflection": reflection_data.get("reflection"),
        "completed_at": completed_at_str
    }

@router.post("/reflections", response_model=ReflectionResponse)
async def generate_reflection_standalone(req: ReflectionRequest):
    """Generate standalone AI reflection."""
    reflection = await mission_generator.generate_reflection(
        object_name=req.object_name,
        category=req.category,
        mission_title=req.mission_title,
        user_observation=req.user_observation,
        field_time_seconds=req.field_time_seconds
    )
    return ReflectionResponse(**reflection)

@router.get("/grass-score", response_model=GrassScoreResponse)
async def get_grass_score(
    screen_time: int = Query(..., description="Screen time in seconds"),
    field_time: int = Query(..., description="Field time in seconds"),
    has_observation: bool = Query(True),
    observation: Optional[str] = Query(None),
    is_completed: bool = Query(True)
):
    """Calculate explainable grass score metrics with detailed 4-part breakdown."""
    metrics = calculate_grass_score(
        screen_time_seconds=screen_time,
        field_time_seconds=field_time,
        user_observation=observation,
        has_observation=has_observation,
        is_completed=is_completed
    )
    return GrassScoreResponse(**metrics)

@router.get("/journal")
async def get_journal(limit: int = 50, db: Session = Depends(get_db)):
    """Fetch past exploration journal entries from local SQLite."""
    entries = JournalService.list_journal_entries(db=db, limit=limit)
    return [
        {
            "id": e.id,
            "created_at": e.created_at.isoformat(),
            "completed_at": e.completed_at.isoformat() if e.completed_at else None,
            "object_name": e.object_name,
            "category": e.category,
            "confidence": e.confidence,
            "uncertainty": e.uncertainty,
            "mission_title": e.mission_title,
            "mission_instruction": e.mission_instruction,
            "mission_why": e.mission_why,
            "observation_goal": e.observation_goal,
            "screen_time_seconds": e.screen_time_seconds,
            "field_time_seconds": e.field_time_seconds,
            "grass_score": e.grass_score,
            "ratio": e.ratio,
            "user_observation": e.user_observation,
            "ai_reflection": e.ai_reflection,
            "curiosity_fact": e.curiosity_fact,
            "next_suggestion": e.next_suggestion,
            "image_url": e.image_url
        }
        for e in entries
    ]

@router.get("/stats")
async def get_exploration_stats(db: Session = Depends(get_db)):
    """Return lifetime field stats."""
    return JournalService.get_stats(db=db)


# --- Botanical Encyclopedia & Plant Database Endpoints ---

@router.get("/plants/categories")
async def get_plant_categories(db: Session = Depends(get_db)):
    """Return all available plant categories and their species counts."""
    return PlantService.get_categories(db=db)


@router.get("/plants/search")
async def search_plants(
    q: str = Query(..., description="Search query across scientific, common, Hindi, Bengali names, or traits"),
    category: Optional[str] = Query(None, description="Optional category filter"),
    limit: int = Query(50, ge=1, le=150, description="Max results"),
    db: Session = Depends(get_db)
):
    """Search botanical database across multiple indices (canonical, common, Hindi, Bengali, traits)."""
    return PlantService.search_plants(db=db, query_str=q, category=category, limit=limit)


@router.get("/plants/match/{name}")
async def match_plant_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    """Look up a botanical profile by scientific or common name."""
    plant = PlantService.get_plant_by_scientific_name(db=db, name=name)
    if not plant:
        # Try search fallback
        results = PlantService.search_plants(db=db, query_str=name, limit=1)
        if results:
            return results[0]
        raise HTTPException(status_code=404, detail=f"No botanical profile found matching '{name}'")
    return plant


@router.get("/plants/{plant_id}")
async def get_plant_detail(
    plant_id: str,
    db: Session = Depends(get_db)
):
    """Fetch complete botanical profile for a specific plant species by ID."""
    plant = PlantService.get_plant_by_id(db=db, plant_id=plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail=f"Plant species '{plant_id}' not found in encyclopedia")
    return plant


@router.get("/plants")
async def list_plants(
    category: Optional[str] = Query(None, description="Filter by category (medicinal, flower, tree, fruit, etc.)"),
    growth_type: Optional[str] = Query(None, description="Filter by growth type (herb, shrub, tree, climber, etc.)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(120, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """List plant species in the encyclopedia with optional filtering."""
    return PlantService.list_plants(db=db, category=category, growth_type=growth_type, skip=skip, limit=limit)

