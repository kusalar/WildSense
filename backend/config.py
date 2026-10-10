import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load .env if present from project root or backend dir
load_dotenv(BASE_DIR / ".env")
load_dotenv(Path(__file__).parent / ".env")
load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'wildsense.db'}")

# Ollama / AI Model Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
REASONING_PROVIDER = os.getenv("REASONING_PROVIDER", "ollama")

# Active reasoning model: can be set to gemma2:2b or qwen3:4b
REASONING_MODEL = os.getenv("REASONING_MODEL", os.getenv("OLLAMA_MODEL", "qwen3:4b"))
GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma2:2b")

# Backward compatibility alias
DEFAULT_MODEL = REASONING_MODEL

# Configurable vision model: defaults to moondream
VISION_MODEL = os.getenv("VISION_MODEL", "moondream")

# Feature flag for Stage 5 Indian Flora Specialist Arbitration (disabled by default)
ENABLE_INDIAN_FLORA_SPECIALIST = os.getenv("ENABLE_INDIAN_FLORA_SPECIALIST", "false").lower() in ("true", "1", "yes")

# Server Configuration (0.0.0.0 allows access from local machine and phone on Wi-Fi)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Audio / TTS Configuration (Task 6)
AUDIO_PROVIDER = os.getenv("AUDIO_PROVIDER", "browser").lower().strip()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5").strip()
ELEVENLABS_TIMEOUT_SECONDS = float(os.getenv("ELEVENLABS_TIMEOUT_SECONDS", "15.0"))

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.0.193:3000",
    "http://192.168.0.193:8000",
    "*"
]

