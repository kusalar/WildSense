# WildSense Stage 7 — Release Readiness Checklist

> **Purpose**: Final pre-release verification matrix for hackathon evaluation, judge demonstrations, and public release.  
> **Environment**: Windows 10/11, Python 3.11+, Node.js 18+, Local CPU Inference  
> **Target Release Mode**: Production Baseline (`ENABLE_INDIAN_FLORA_SPECIALIST=false`)

---

## 📋 Comprehensive Release Verification Matrix

| # | Audit Category | Specific Check / Item | Verification Command / Step | Expected Result | Verified Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| **1** | **Setup & Env** | Clean dependencies & virtualenv | `pip install -r requirements.txt` | Clean install; no missing dependencies | **PASS** |
| **2** | **Model Assets** | ONNX and taxonomy files present | Verify `backend/models_onnx/` | `flora_student_fp32.onnx` (44.8 MB), `taxa_table.npy` (16.7 MB), `taxa_labels.json` (301 KB) present | **PASS** |
| **3** | **API Health** | `/health` endpoint responds correctly | `curl http://127.0.0.1:8000/health` | `status: "healthy"`, `onnx_available: true`, `specialist_enabled: false` | **PASS** |
| **4** | **Test Suite** | Full backend test pass rate | `pytest -v` | **79 passed, 0 failed** in ~38s | **PASS** |
| **5** | **Frontend Build** | Production TypeScript & static build | `cd frontend; npm run build` | Compiled successfully; 4/4 static routes generated with 0 errors | **PASS** |
| **6** | **Phone Access** | Local Wi-Fi network accessibility | Open `http://<HOST_IP>:3000` on mobile | UI renders smoothly; camera file input opens native camera | **PASS** |
| **7** | **Offline Inference**| Zero external cloud image calls | Disconnect internet & identify specimen | Full recognition completes in <100ms via local ONNX CPU | **PASS** |
| **8** | **Privacy** | In-memory volatility of user photos | Inspect disk during/after upload | No temporary uploaded image files persisted to persistent storage | **PASS** |
| **9** | **No Regression** | Global baseline on controls | Recognize `lotus.jpg`, `water_lily.jpg` | Sacred Lotus identified at 0.67; Water Lily at 0.69 | **PASS** |
| **10**| **Flag Guard** | Specialist feature flag default | Inspect `config.py` & `.env.example` | `ENABLE_INDIAN_FLORA_SPECIALIST=false` is default in all configurations | **PASS** |
| **11**| **Database** | Preserve existing user records | Inspect `data/wildsense.db` | 114 native species and existing exploration sessions preserved | **PASS** |
| **12**| **Licensing** | Commercial restriction disclosure | Review `README.md` & `metadata.json` | 89.5% non-commercial research licensing clearly disclosed | **PASS** |

---

## 🔍 Detailed Verification Procedures

### 1. API Health & Configuration Verification
Execute via PowerShell:
```powershell
python -c "import backend.main as main; from fastapi.testclient import TestClient; client = TestClient(main.app); res = client.get('/health'); print(res.status_code, res.json())"
```
**Verification Criteria**:
- HTTP Status: `200`
- `onnx_available`: `True`
- `specialist_available`: `True`
- `specialist_enabled`: `False` (Confirms specialist is kept safe behind feature flag).

---

### 2. Regression & Baseline Botanical Recognition Check
Verify that the global model maintains accuracy on established controls:
```powershell
# Lotus Control
python -c "import backend.main as main; from fastapi.testclient import TestClient; client = TestClient(main.app); f = open('test_specimens/lotus.jpg', 'rb'); res = client.post('/api/recognize', files={'images': ('lotus.jpg', f, 'image/jpeg')}, data={'organ_type': 'flower'}); print(res.json()['scientific_name'], res.json()['similarity_score'])"

# Water Lily Control
python -c "import backend.main as main; from fastapi.testclient import TestClient; client = TestClient(main.app); f = open('test_specimens/water_lily.jpg', 'rb'); res = client.post('/api/recognize', files={'images': ('water_lily.jpg', f, 'image/jpeg')}, data={'organ_type': 'flower'}); print(res.json()['scientific_name'], res.json()['similarity_score'])"
```
**Verification Criteria**:
- Lotus returns `Nelumbo nucifera` with similarity $\ge 0.65$.
- Water Lily returns `Nymphaea nouchali` (or genus `Nymphaea`) with similarity $\ge 0.65$.
- Neither is overridden by the specialist head.

---

### 3. Dual-Model Arbitration Benchmark Reproduction
Verify the Stage 5/6 arbitration benchmark:
```powershell
python evaluate_arbitration.py
```
**Verification Criteria**:
- On 28 held-out test specimens, the specialist is accepted on 13 specimens and abstains on 15.
- Accuracy among accepted specialist predictions is **13 / 13 (100.0%)**.
- Results match `data/specialist_dataset/stage6_benchmark_results.json`.

---

### 4. Database Integrity Verification
Ensure SQLite database schema and historical records are preserved:
```powershell
python -c "import sqlite3; con = sqlite3.connect('data/wildsense.db'); cur = con.cursor(); print('Plants:', cur.execute('SELECT COUNT(*) FROM plants').fetchone()[0]); print('Sessions:', cur.execute('SELECT COUNT(*) FROM sessions').fetchone()[0])"
```
**Verification Criteria**:
- Plants count: `114`
- Exploration sessions: preserved (non-zero).
- No tables dropped or truncated.

---

### 5. Frontend Production Build Check
Ensure TypeScript type safety and production asset compilation:
```powershell
cd frontend
npm run build
cd ..
```
**Verification Criteria**:
- Compilation finishes in under 2 seconds.
- 0 TypeScript errors.
- 4/4 static routes generated.

---

### 6. Mobile Network & Local Wi-Fi Field Readiness
1. Run `ipconfig` in PowerShell to find host IP (e.g., `192.168.0.x`).
2. Run frontend with `npm run dev -- -H 0.0.0.0` or `npm run start -- -H 0.0.0.0`.
3. Load `http://<HOST_IP>:3000` on mobile Safari or Chrome.
4. Verify that camera capture opens without crashing and the navigation bar scales properly.

---

## ⚠️ Pre-Demo Sanity Reminders

- [ ] **Do NOT run `git checkout -- data/wildsense.db`** (preserves existing exploration history).
- [ ] **Do NOT enable `ENABLE_INDIAN_FLORA_SPECIALIST=true` by default** unless specifically demonstrating regional specialist arbitration.
- [ ] **Do NOT make commercial readiness claims** for the specialist due to CC-BY-NC image licenses.
- [ ] Disclose Sweet Basil vs. Tulsi vegetative lookalike limitations if asked by judges.
