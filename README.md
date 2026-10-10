# WildSense 🌿
> **Look closer. Then look away.**  
> *Offline-First Local AI Nature Exploration Companion for the "Touch Grass" Challenge.*

---

## 🎯 The Core Philosophy & The Problem

Modern smartphones and algorithmic feeds have detached people from the living physical world. Even nature identification apps frequently trap users in their screens—demanding endless scrolling, social feeds, gamified streaks, and cloud uploads.

**WildSense does the exact opposite.**
- **The Core Goal**: Minimize screen time and maximize real-world physical engagement with nature.
- **Anti-Gamification**: No streaks, no social leaderboards, no push notifications, no attention-seeking dark patterns.
- **The Touch Grass Mantra**: WildSense is a bridge to the outdoors. The app succeeds when you put your phone in your pocket.

```text
       📷 REAL WORLD
             ↓
    LOCAL BOTANICAL AI
      "What is this?"
             ↓
     PHYSICAL MISSION
  "What can I investigate?"
             ↓
      📵 PHONE IN POCKET
             ↓
     🌿 REAL SENSORY TIME
             ↓
         REFLECT
             ↓
     🌎 EXPLAINABLE SCORE
```

> **"WildSense succeeds when you stop using WildSense."**

---

## ✨ Main Features

1. **Local FastViT Botanical Identification (4,271 Taxa)**:
   - Evaluates specimens completely offline on local CPU using a distilled FastViT image encoder (`flora_student_fp32.onnx`) and a 4,271-class botanical embedding space (`taxa_table.npy`).
   - Generates top-5 candidate rankings with scientific names, common names, regional vernacular names (Hindi, Bengali, Tamil), and calibrated similarity metrics.
2. **Multi-Photo & Organ-Type Guidance**:
   - Accepts up to 3 photographs of a specimen with botanical organ selection (**Leaf**, **Flower**, **Fruit**, **Bark**, **Whole Plant**).
   - Fuses multi-view feature vectors into an L2-normalized mean embedding for higher diagnostic stability.
3. **Deterministic Image Quality Safeguards**:
   - Pre-flight optical checks inspect image resolution, under/overexposure, and pixel variance to warn against blurry or blank inputs.
4. **Offline Botanical Encyclopedia (114 Native Species)**:
   - Built-in SQLite database of regional trees, medicinal herbs, shrubs, and wildflowers.
   - Provides diagnostic traits, ecological roles, and traditional uses with full search and category filtering.
5. **Contextual Physical Missions**:
   - Generates 2–3 minute sensory exploration missions adhering strictly to the **10 Nature Mission Safety Rules** (no damaging plants, no touching hazardous species, sensory curiosity over screen consumption).
6. **Phone-Free Field Mode & Spoken Narration**:
   - Minimalist screen-off field timer.
   - Hands-free audio mission narration powered either by **100% offline Browser Web Speech API** or high-fidelity **ElevenLabs Flash v2.5**.
7. **Explainable Grass Score**:
   - Transparent 0–100 score measuring how effectively the user traded screen time for outdoor exploration.
   - 70% World/Screen Ratio + 15% Mission Completion + 10% Phone-Free Field Time + 5% Sensory Reflection.
8. **Private SQLite Field Journal**:
   - Stores exploration logs, reflections, and discovery milestones locally on disk. Zero cloud database requirements.
9. **Regional Indian Flora Specialist (Dual-Model Arbitration)**:
   - High-precision classifier (`indian_flora_specialist.npz`) targeting regional flora: **Neem**, **Tulsi**, **Marigold**, **Shiuli**, **Palash**, **Moringa**, and **Rose**.
   - Governed by a strict 5-gate safety arbitrator (`ENABLE_INDIAN_FLORA_SPECIALIST=false` by default for maximum release stability).

---

## 🏛️ High-Level Architecture Overview

WildSense is structured into three clean, loosely-coupled layers:

```text
┌──────────────────────────────────────────────────────────────────┐
│                   NEXT.JS 16 FRONTEND (PORT 3000)                │
│  • Mobile-first responsive UI (React 19, TypeScript, Tailwind)   │
│  • Camera capture (1-3 photos) with Organ Selector               │
│  • Field Mode timer, Speech synthesis, Offline Encyclopedia      │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ HTTP / JSON & Multipart
┌─────────────────────────────────▼────────────────────────────────┐
│                   FASTAPI BACKEND (PORT 8000)                    │
│  • Deterministic Image Quality Pre-Flight Checks                 │
│  • FastViT ONNX Runtime Inference (512-dim embedding extraction) │
│  • Cosine Similarity vs 4,271 Taxonomy Centroids                 │
│  • Optional 5-Gate Specialist Arbitrator (Feature-Flagged)       │
│  • Contextual Mission Engine & Grass Score Calculator            │
│  • SQLite Local Database & Journal Service                       │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────┐
│                     LOCAL STORAGE & ASSETS                       │
│  • backend/models_onnx/flora_student_fp32.onnx (44.8 MB)         │
│  • backend/models_onnx/taxa_table.npy (4,271 classes, 16.7 MB)   │
│  • backend/models_onnx/taxa_labels.json (301 KB)                 │
│  • data/specialist_dataset/indian_flora_specialist.npz (28 KB)   │
│  • data/wildsense.db (SQLite database: 114 plants, sessions)     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 💻 Technology Stack & AI Models

| Component | Technology | Role & Deployment |
| :--- | :--- | :--- |
| **Frontend** | Next.js 16.4 (React 19, TypeScript, Tailwind CSS) | Mobile-first field UI, PWA-ready, runs on port 3000 |
| **Backend** | Python 3.11+, FastAPI, Uvicorn | Asynchronous REST API, runs on port 8000 |
| **Vision AI Engine** | FastViT ONNX Runtime (`flora_student_fp32.onnx`) | Distilled botanical vision model, 512-dim L2 embeddings |
| **Global Taxonomy** | NumPy Array (`taxa_table.npy`) | 4,271 global botanical taxon vectors |
| **Indian Flora Specialist** | NumPy Centroids + Logistic Regression | 7 regional target species (`indian_flora_specialist.npz`) |
| **Text Reasoning (Optional)** | Ollama (`qwen3:4b` / `gemma2:2b`) or Heuristic Mock | Mission generation and botanical reflection |
| **Audio Engine** | Web Speech API (offline) or ElevenLabs API | Spoken mission instructions for eyes-free exploration |
| **Database** | SQLite + SQLAlchemy (`wildsense.db`) | 114 botanical profiles, user exploration journal |

> **IMPORTANT CLARIFICATION**:  
> **Ollama is NOT required for botanical plant recognition.**  
> Plant identification runs 100% offline via local ONNX Runtime and NumPy embedding dot products. Ollama is only used as an optional text-generation backend for exploration missions; if Ollama is not installed or running, WildSense automatically uses its built-in rule-based mission engine without degradation.

---

## 🚀 Windows Setup Guide

### 1. Prerequisites
- **Python 3.11+** installed (check with `python --version`)
- **Node.js 18+** & **npm** installed (check with `node --version`)
- **Windows PowerShell** or Windows Terminal
- *(Optional)* [Ollama](https://ollama.ai) if you wish to run local LLMs for mission text.

### 2. Clone and Configure Environment
From your terminal:
```powershell
# Navigate to project directory
cd C:\wildsense

# Copy environment template
Copy-Item .env.example .env
```

### 3. Backend Setup
```powershell
# Recommended: Create and activate a Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r requirements.txt
```

Verify that the required ONNX assets exist in `backend/models_onnx/`:
- `flora_student_fp32.onnx` (~44.8 MB)
- `taxa_table.npy` (~16.7 MB)
- `taxa_labels.json` (~301 KB)

*(These are included directly in the repository).*

### 4. Frontend Setup
In the `frontend` directory:
```powershell
cd frontend
npm install
cd ..
```

---

## 🏃 Running the Application

Open **two separate PowerShell terminals**:

### Terminal 1 — Backend API
```powershell
cd C:\wildsense
# Activate venv if created: .\.venv\Scripts\Activate.ps1
python backend/main.py
```
- API starts at `http://127.0.0.1:8000` (and `http://0.0.0.0:8000`).
- Health check available at `http://127.0.0.1:8000/health`.
- Interactive OpenAPI docs at `http://127.0.0.1:8000/docs`.

### Terminal 2 — Frontend Development Server
```powershell
cd C:\wildsense\frontend
npm run dev -- -H 0.0.0.0
```
- Web application opens at `http://localhost:3000`.
- The `-H 0.0.0.0` flag binds the dev server to all network interfaces, allowing phones on your local Wi-Fi to connect.

---

## 📱 Mobile Field Testing Instructions

WildSense is designed as a **mobile field companion**. To test it on your physical phone:

1. **Connect to the Same Wi-Fi**: Ensure your smartphone and development laptop are on the same local Wi-Fi network.
2. **Find Your Laptop's Local IP**:
   In PowerShell, run:
   ```powershell
   ipconfig
   ```
   Look for `IPv4 Address` under your active Wi-Fi adapter (e.g., `192.168.0.193`).
3. **Open on Phone Browser**:
   Open Chrome or Safari on your phone and navigate to:
   ```text
   http://192.168.0.193:3000
   ```
   *(Replace with your actual IP address).*
4. **Dynamic API Routing**:
   WildSense's API client automatically detects `window.location.hostname` and routes backend requests directly to `http://192.168.0.193:8000/api`.
5. **Camera Access**:
   Tap **"Take Photo"** on the mobile screen to trigger your phone's native camera via HTML5 file capture (`capture="environment"`).

---

## 🔒 Privacy & Local Processing Guarantee

- **Zero Cloud Image Uploads**: Specimen photographs are never transmitted to external cloud APIs or remote tracking services.
- **In-Memory Stream Processing**: Images are processed directly in RAM via `io.BytesIO` streams and immediately released. They are not permanently stored on disk unless explicitly logged by the user into the local journal.
- **Offline Telemetry-Free Design**: All SQLite journal records, exploration history, and Grass Scores stay exclusively on the host device.

---

## ⚠️ Model Provenance, Licensing & Known Limitations

### 1. Research Licensing Notice
- The Indian Flora Specialist was trained on 133 curated botanical images from iNaturalist (`data/specialist_dataset/`).
- **License Distribution**: 88.0% `CC-BY-NC`, 8.3% `CC-BY`, 1.5% `CC-BY-NC-SA`, 1.5% `CC-BY-SA`, 0.8% `CC0`.
- **Usage Restriction**: Because 89.5% of images carry Non-Commercial restrictions, **the specialist weights are strictly for educational hackathons, open research, and demonstration purposes**. They must not be deployed commercially without relitigating training asset licenses.

### 2. Recognition Limitations & Abstention
- **Conservative Dev Thresholds**: The specialist's multi-gate arbitration policy enforces high acceptance thresholds ($\tau \ge 0.68\text{--}0.72$) and a strict margin gate ($\Delta \ge 0.035$). It prioritizes safety over raw coverage: on unseen test specimens, it achieves **100% precision (13/13)** among accepted predictions, but safely abstains on 53.6% of images, falling back to the global model.
- **Sweet Basil vs. Tulsi Ambiguity**: Vegetative leaves of Sweet Basil (*Ocimum basilicum*) and Holy Basil / Tulsi (*Ocimum tenuiflorum*) share high visual similarity. The system flags Tulsi as `genus_confirmed` and attaches an explicit floral spike warning rather than asserting false certainty.
- **Optical Checks vs. Botanical Content**: Pixel variance checks flag blank or underexposed surfaces, but **textured non-plants** (e.g. granite rocks, brick walls) pass variance filters. WildSense relies on similarity score thresholds and epistemic uncertainty warnings, not an infallible non-plant classifier.

### 3. Production Configuration
- `ENABLE_INDIAN_FLORA_SPECIALIST=false` is set by default in [`.env.example`](file:///c:/wildsense/.env.example) and [`backend/config.py`](file:///c:/wildsense/backend/config.py). The production release relies on the proven 4,271-taxa global baseline.

---

## 🧪 Verification & Automated Testing

Run the full verification suite locally:

```powershell
# 1. Run backend unit and integration test suite (79 tests)
pytest -v

# 2. Reproduce the Stage 6 dual-model arbitration benchmark
python evaluate_arbitration.py

# 3. Test frontend production build
cd frontend
npm run build
cd ..
```

---

## 📄 License & Attribution

- **Application Code**: MIT License.
- **Global Vision Model**: FastViT botanical vision backbone distilled on open botanical datasets.
- **Specialist Dataset**: Curated from iNaturalist under research licenses (CC-BY-NC / CC-BY). See [`data/specialist_dataset/metadata.json`](file:///c:/wildsense/data/specialist_dataset/metadata.json) for individual photographer attributions and license URLs.
