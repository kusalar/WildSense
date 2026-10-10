# WildSense 🌿
> **Look closer. Then look away.**  
> *Offline-First AI Nature Exploration Companion for the "Touch Grass" Challenge.*

---

## 🎯 The Core Philosophy

WildSense is not a generic chatbot, an endless social feed, or another app designed to steal your attention.

**The goal of WildSense is to minimize screen time and maximize real-world physical engagement with nature.**

```text
📷 REAL WORLD
      ↓
LOCAL VISION
"What is this?"
      ↓
🧠 GEMMA / QWEN
"What should I try?"
      ↓
📵 PHONE AWAY
      ↓
🌿 EXPLORE
      ↓
REFLECT
      ↓
🌎 GRASS SCORE
```

> **"WildSense succeeds when you stop using WildSense."**

WildSense does not need a remote AI service to decide what someone should do outdoors.

The reasoning model runs locally.

The user's image can stay local.

The mission can be generated locally.

The experience can continue without sending personal observations to a cloud AI provider.

---

## 🌎 Grass Score: An Explainable, Evidence-Based Metric

**Grass Score is not an engagement score.** It does not reward screen time, app opens, or habitual usage. Instead, it measures whether WildSense successfully helped someone **trade screen time for real-world physical exploration**.

### 1. Philosophy & Anti-Gamification
- **Rewards**: LESS SCREEN + MORE WORLD + ACTUAL ACTION + REFLECTION.
- **Strictly Avoids Dark Patterns**:
  - ❌ No streaks requiring daily app usage
  - ❌ No addictive push notifications
  - ❌ No infinite feeds or algorithmic scrolling
  - ❌ No competitive leaderboards or social comparison
  - ❌ No engagement badges encouraging app screen time
- **Guiding Principle**: Grass Score is an honest reflection metric, not an engagement trap. WildSense succeeds when the user puts the phone away.

### 2. Weighted Formula (Bounded: 0 to 100 Points)

The score is calculated deterministically across four independent, measurable behaviors:

```text
GRASS SCORE = 
  70%  World / Screen Ratio      (0 to 70 pts)
  15%  Mission Completion         (0 or 15 pts)
  10%  Phone-Free Field Time      (0 to 10 pts)
   5%  Reflection                 (0 to 5 pts)
─────────────────────────────────────────────────
Total: 100 points maximum (clamped between 0 and 100)
```

#### Component 1: World / Screen Ratio (70%)
- **Formula**: `ratio = world_time_seconds / max(screen_time_seconds, 1)`
- **Piecewise Interpolation** prevents extreme ratios from arbitrarily outputting 100:
  - `< 1×` → 10 base points
  - `1×` → 25 base points (`17.5` weighted pts)
  - `3×` → 55 base points (`38.5` weighted pts)
  - `5×` → 70 base points (`49.0` weighted pts)
  - `10×` → 90 base points (`63.0` weighted pts)
  - `20× or higher` → 100 base points (`70.0` max weighted pts)
- **Component Contribution**: `ratio_score = mapped_ratio_points * 0.70` (max 70).

#### Component 2: Mission Completion (15%)
- **Award**: `15 points` if the field session is finished and completed; `0 points` if abandoned.
- Points are never awarded merely for generating a mission.

#### Component 3: Phone-Free Field Time (10%)
- **Bounded Scale** rewarding meaningful time outdoors without screen intervention:
  - `0s` → 0 pts
  - `30s` → 3 pts
  - `60s` → 5 pts
  - `120s` → 7 pts
  - `300s` → 8.5 pts
  - `600s+` → 10 pts (capped at 10 max)

#### Component 4: Reflection (5%)
- **Tiers**:
  - Empty / none → 0 pts
  - Very short (<15 chars) → 2 pts
  - Meaningful physical observation → 4 pts
  - Meaningful observation + curiosity / question (`?`, `why`, `how`, `wonder`) → 5 pts

### 3. Example E2E Case (6.87× Ratio)
```text
World Time: 261s (04:21)
Screen Time: 38s (00:38)
World / Screen Ratio: 6.87×
Mission: Completed
Phone-Free Time: 261s
Reflection: Meaningful observation ("underside had lighter green with prominent raised veins")

SCORE BREAKDOWN:
🌿 World / Screen Ratio: 55 / 70
✓ Mission Completed:     15 / 15
📵 Phone-Free Time:       8 / 10
💭 Reflection:            4 / 5
───────────────────────────────
TOTAL:                   82 / 100 (True Field Naturalist 🌿)
```
Notice that a 6.9× ratio does **not** arbitrarily produce 100; it produces a realistic, explainable **82 / 100**.

---

## 🔬 Model Separation & Architecture

WildSense strictly separates the vision classification pipeline from the reasoning and mission generation pipeline:

```
Camera Image / Photo
         ↓
VisionProvider (OllamaVisionProvider / MockVisionProvider)
         ↓
Structured Recognition (Category, Name, Confidence, Epistemic Uncertainty)
         ↓
AIProvider / LLM (OllamaProvider with Qwen3:4b or Gemma3:4b)
         ↓
MissionGenerator (Phone-Free Physical Observation Mission)
         ↓
Phone-Free Field Mode (Timer running, phone in pocket)
         ↓
Observation & Reflection
         ↓
Grass Score (SQLite Journal)
```

### 1. Vision Model: "What is this?"
- **Role**: Identifies the biological kingdom or morphological category (leaf, flower, tree, rock, insect, etc.), estimates approximate common name, evaluates confidence, and produces epistemic uncertainty notes.
- **Configured Vision Model**: `moondream` (Ollama, ~829 MB, 1.4B parameters).
- **Vision Provider Abstraction**:
  - `OllamaVisionProvider`: Communicates with local Ollama daemon using in-memory base64 encoded images. Zero cloud calls.
  - `MockVisionProvider`: Genuine local in-memory computer vision using PIL spectral and chromatic band heuristics. Analyzes chlorophyll green ratios, floral pigment peaks, and mineral textures in ~5–15 ms without any model downloads.

### 2. Reasoning LLM: "What should I try?"
- **Role**: Takes the structured recognition output and synthesizes a safe, phone-free physical investigation mission and post-walk reflection.
- **Configured Model**: `qwen3:4b` (Ollama open-weight model, ~2.5 GB, 4.0B parameters).
- **Crucial Distinction**: `Qwen3:4b` is an open-weight text reasoning model, **NOT** a computer vision model. It answers "What should the observer investigate with their own senses?", not "What does the image contain?".

---

## 💻 Hardware Considerations & Performance

Tested on a real-world everyday developer laptop:
- **Operating System**: Windows 10
- **CPU**: 11th Gen Intel Core i3-1115G4 (2 physical cores, 4 threads @ 3.00 GHz)
- **RAM**: 12 GB Total (~4.5 GB available physical memory)
- **GPU**: Intel UHD integrated graphics (CPU-only inference mode)
- **Storage**: SSD (118 GB available)

### Performance & Latency Metrics
- **Local CV In-Memory Heuristic Inference**: ~5–15 ms
- **Local Ollama Text LLM (`qwen3:4b`) Generation**: ~1.5s–15s on CPU (~7–10 tokens/second)
- **Total Pipeline Latency**: ~1.5s–16s from camera capture to structured mission preview
- **RAM Footprint**: `qwen3:4b` consumes ~2.6 GB RAM during inference. Running on a 12 GB RAM laptop leaves ample headroom for OS and background tasks without disk thrashing.

---

## 🛡️ Epistemic Honesty & Fallback Chain

WildSense adheres to strict epistemic modesty:
1. **Never Claim False Certainty**: Instead of "THIS IS DEFINITELY NEEM", WildSense reports: *"Likely Neem Leaf — 74% confidence. Visual identification is approximate."*
2. **3-Tier Resilient Fallback Chain**:
   ```
   Local Ollama Vision Model (e.g. moondream)
             ↓ [if unavailable or uninstalled]
   Local In-Memory Spectral CV Analyzer (MockVisionProvider)
             ↓ [if image unreadable or corrupted]
   Unknown Nature Object Safety Fallback
   ```
3. **Honest Provider Labeling**: When fallback heuristics run, the system labels the provider as `local_cv_fallback` rather than faking neural network results.

---

## Why Open AI Matters

WildSense is designed around interchangeable local models.

The application does not depend on a single proprietary AI API.

A local vision model handles perception.

An open-weight reasoning model such as Gemma or Qwen handles mission generation.

The safety and scoring layers remain deterministic application code.

This means researchers and developers can inspect, replace, benchmark, and improve each part independently.

The result is not just an AI application.

It is an open architecture for turning AI into a bridge toward the physical world.

---

## 🔒 Privacy & Local Processing Guarantee

- **Zero Cloud Image Processing**: Camera images are processed strictly on localhost (`127.0.0.1`). No cloud vision APIs, remote endpoints, or tracking servers are ever contacted.
- **In-Memory Volatility**: Images are validated and analyzed directly in memory via byte streams (`io.BytesIO`). They are never permanently saved to disk or exposed to external services.

---

## 🎙️ Voice Missions: ElevenLabs & Offline Audio Integration (Task 6)

> **"The best interface for a nature mission is one that lets you stop looking at the interface."**

In digital wellness, audio is a bridge. Rather than reading text on a glass screen, users listen to a calm, 15–30 second spoken mission instruction, pocket their device, and engage their eyes and hands directly with the living world.

```text
       [ Approved Mission ]
                 ↓
  format_mission_narration()
  (Title • Duration • Action • Goal • Safety)
                 ↓
      ┌──────────────────────┐
      │   Provider Router    │
      └──────────┬───────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
[ ElevenLabs API ]   [ Browser Web Speech ]
• High-Fidelity TTS  • 100% Offline & Private
• Flash v2.5 Model   • Zero External Network
• In-Memory Audio    • Instant SpeechSynthesis
        │                 │
        └────────┬────────┘
                 ▼
       [ User Listens ]
                 ↓
       [ PHONE IN POCKET ]
```

### 1. Architectural Highlights
- **Optional Online Enhancement**: WildSense reasoning (Gemma/Qwen), local vision (Moondream/CV), and journal persistence (SQLite) remain 100% offline. ElevenLabs is an optional voice upgrade.
- **Genuine API Integration**: Calls the official ElevenLabs Text-to-Speech API (`POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`) using the low-latency `eleven_flash_v2_5` model.
- **In-Memory Audio Processing**: Audio bytes are synthesized directly in RAM and transmitted via base64 data URIs or binary responses (`audio/mpeg`). No audio files are written to persistent disk.
- **Graceful Deterministic Fallback**: If ElevenLabs is unconfigured, rate-limited (`429`), unauthorized (`401`), or offline, WildSense immediately falls back to local browser speech synthesis (`window.speechSynthesis`) with an honest, transparent status badge.
- **Strict Data Isolation**: Specimen photographs, location coordinates, SQLite journals, and personal reflections are **never** transmitted to ElevenLabs. Only the concise spoken mission instruction is sent.

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure audio settings in `.env`:
```env
# Options: "browser" (default offline speech synthesis) or "elevenlabs"
AUDIO_PROVIDER=elevenlabs

# Optional ElevenLabs Settings (Do not commit secrets to git)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
ELEVENLABS_MODEL_ID=eleven_flash_v2_5
```

### 3. Voice Endpoints
- `GET /api/audio/status`: Returns current provider readiness, voice configuration, and browser speech support without exposing secrets.
- `POST /api/audio`: Generates mission narration. Accepts either raw text or structured mission parameters (`title`, `instruction`, `physical_action`, `observation_goal`, `safety_note`, `estimated_minutes`). Returns playback cues and in-memory audio data URIs.
- `POST /api/audio/raw`: Streams binary `audio/mpeg` bytes directly for native audio players.

### 4. Verification & Testing
- **Unit Tests with Mocks (No API Key Required)**:
  ```bash
  pytest backend/tests/test_wildsense.py -v
  ```
  Runs 44 unit tests covering configuration defaults, request construction, error handling, rate limiting, timeout handling, safe fallbacks, content types, and privacy isolation.
- **End-to-End Pipeline Verification**:
  ```bash
  python test_e2e.py
  ```
  Validates the full 9-step pipeline: Health -> Vision -> Recognition -> Session -> Mission -> Audio (Browser & ElevenLabs branches) -> Grass Score -> SQLite Journal.
- **Live ElevenLabs API Verification**:
  Tested and verified against live ElevenLabs API (`eleven_flash_v2_5` with voice `EXAVITQu4vr4xnSDxMaL`) producing valid `audio/mpeg` streams in real time.

---

## 🏛️ System Architecture

```
wildsense/
├── frontend/               # Next.js 16 (React 19, TypeScript, Tailwind CSS)
│   ├── app/
│   │   ├── page.tsx        # Mobile-First Field Companion UI (Camera, Field Mode, Audio Guide)
│   │   ├── layout.tsx      # Viewport & Metadata setup
│   │   └── globals.css     # Organic nature styling & tokens
│   ├── lib/
│   │   └── api.ts          # Resilient API client (multipart recognition & audio providers)
│   └── package.json
├── backend/                # Python FastAPI server
│   ├── main.py             # App entrypoint & lifespan events
│   ├── config.py           # Model and environment configurations (.env supported)
│   ├── database.py         # Local SQLite engine
│   ├── models.py           # SQLAlchemy session & journal schemas
│   ├── api/
│   │   └── routes.py       # REST API endpoints (/health, /recognize, /mission, /audio, etc.)
│   └── services/
│       ├── audio_provider.py # ElevenLabsAudioProvider, BrowserAudioProvider, format_mission_narration
│       ├── vision_provider.py # VisionProvider, OllamaVisionProvider, MockVisionProvider
│       ├── recognizer.py   # Pluggable nature CV recognizer & demo presets
│       ├── ai_provider.py  # Modular AIProvider & MockProvider
│       ├── ollama_provider.py # Local Ollama connector (think: false, configurable model)
│       ├── mission_generator.py # Physical observation mission generator (10 safety rules)
│       ├── grass_score.py  # World / Screen ratio calculation
│       └── journal.py      # SQLite journal manager
├── data/
│   └── wildsense.db        # SQLite database (Zero cloud required)
├── test_e2e.py             # Complete Task 3-6 end-to-end verification script
└── README.md
```


---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+** & **npm**
- **Ollama** installed locally

### 2. Configure Environment (Optional)
Edit `.env`:
```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:4b
VISION_MODEL=moondream
```

### 3. Start the Backend
```bash
cd backend
python main.py
```
Backend runs at `http://127.0.0.1:8000`.  
Interactive API docs available at `http://127.0.0.1:8000/docs`.

### 4. Start the Frontend
```bash
cd frontend
npm run dev
```
Frontend runs at `http://localhost:3000`.

---

## 🔍 API Endpoints

- `GET /health`: Exposes backend health, Ollama status, configured reasoning model, configured vision model, and `vision_available` flag.
- `POST /api/recognize`: Unified recognition accepting `multipart/form-data` with `image` file or JSON with `preset_id`/`image_base64`.
- `POST /api/mission`: Generates phone-free physical observation missions conforming to the 10 Nature Mission Safety Rules. Includes latency diagnostics (`llm_inference_ms`).
- `POST /api/sessions`: Creates an exploration session in SQLite.
- `POST /api/sessions/{id}/complete`: Concludes session, calculates Grass Score, and stores AI reflection.
- `GET /api/journal`: Retrieves offline field journal history.
- `GET /api/grass-score`: Calculates World-to-Screen engagement ratio.
- `GET /api/stats`: Aggregate lifetime nature discovery statistics.

---

## 🧭 The 10 Nature Mission Rules

All generated missions strictly obey WildSense safety principles:
1. Require physical interaction or observation (inspect, compare, listen, notice).
2. Possible without continuously looking at the phone.
3. Short and focused (2–3 minutes).
4. Encourage curiosity over passive consumption.
5. **Never require damaging nature** (no picking, snapping, or breaking).
6. **Never tell users to eat, touch, collect, or approach potentially hazardous species**.
7. Never disturb wildlife, nests, or burrows.
8. Never require entering dangerous terrain or trespassing.
9. Prefer sensory observation over photography.
10. Strictly avoid generic web search prompts.

---

## ⚠️ Limitations & Hardware Boundaries

1. **Lightweight CPU Vision**: Running large vision models (e.g. `llava:7b` or `llama3.2-vision:11b`) on a dual-core Intel Core i3 without a dedicated GPU causes extreme RAM pressure and >60s latency. For hardware with <= 12 GB RAM, lightweight models (`moondream`, 829 MB) or the built-in local CV in-memory fallback provide the best balance of speed and stability.
2. **Model Swapping on CPU**: If both a vision model and an LLM are configured in Ollama on a system with limited RAM, Ollama will unload and reload weights between `/recognize` and `/mission`. The in-memory `MockVisionProvider` prevents this swap overhead entirely while keeping vision processing local.
