# WildSense 🌿 — 3-Minute Hackathon Demo Script

> **Theme**: Digital Wellness & AI for Good ("Touch Grass" Challenge)  
> **Presenter Target Time**: 3 minutes (180 seconds)  
> **Companion URL**: `http://localhost:3000` (or `http://<YOUR_IP>:3000` on mobile)  
> **Backend URL**: `http://127.0.0.1:8000`

---

## ⏱️ Timeline Overview

| Time | Phase | On-Screen Action | Key Talking Points |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:30** | **The Hook & Problem** | Home Screen (`/`) | Anti-gamification, screen-fatigue, "Touch Grass" philosophy |
| **0:30 – 1:15** | **Live Botanical AI** | Upload specimen (`lotus.jpg` or `neem.jpg`) | FastViT ONNX, multi-photo, organ selection, similarity vs probability |
| **1:15 – 1:45** | **Offline Encyclopedia** | Open "Flora" modal | 114 native species, vernacular names, traditional uses, search |
| **1:45 – 2:20** | **Field Mode & Missions** | Generate mission, listen to audio, lock screen | 10 Safety Rules, Browser TTS / ElevenLabs, phone in pocket |
| **2:20 – 2:45** | **Reflection & Grass Score** | Complete session, type reflection | Explainable 0–100 Grass Score, World/Screen ratio, SQLite journal |
| **2:45 – 3:00** | **Architecture & Honesty** | Architecture overview / Settings | 100% local CPU, specialist arbitration, honest limitations |

---

## 🎙️ Spoken Script & Step-by-Step Directions

---

### [0:00 – 0:30] Phase 1: The Problem & The Hook

**Action on Screen**:
- Start on the WildSense home screen at `http://localhost:3000`.
- Point cursor to the tagline: **"Look closer. Then look away."**

**Spoken Script**:
> *"Judges, almost every nature or plant app created in the past decade does one thing: it traps you in your phone. They give you feeds to scroll, streaks to keep up, and push notifications demanding your attention.*
>
> *We built **WildSense** for the 'Touch Grass' challenge with the exact opposite philosophy: **WildSense succeeds when you stop using WildSense.** It is an offline-first botanical companion designed to get you off your screen and physically interacting with the living world."*

---

### [0:30 – 1:15] Phase 2: Live Botanical Recognition

**Action on Screen**:
- Click **"Start Exploring"** or click on the photo upload zone.
- Select **Flower** or **Leaf** organ button.
- Upload an image (e.g. `test_specimens/lotus.jpg` or `test_specimens/neem.jpg`).
- Click **"Identify Specimen"**.
- The result card appears with **"Sacred Lotus (*Nelumbo nucifera*)"** or **"Neem (*Azadirachta indica*)"**, displaying similarity score, match level, and top 5 botanical candidates.

**Spoken Script**:
> *"Let's test it with an actual specimen. We select the organ type—here, Flower—and upload our photo. 
>
> Notice what happens: there is **zero cloud upload**. In under 100 milliseconds, our local FastViT ONNX model extracts a 512-dimensional embedding and evaluates it against a 4,271-taxa botanical embedding space running entirely on this laptop's CPU.
>
> Notice our epistemic honesty: we label this as a **Similarity Score of 67%**, never a misleading 'probability'. The app also runs optical quality checks to warn if an image is underexposed, blurry, or blank."*

---

### [1:15 – 1:45] Phase 3: Offline Botanical Encyclopedia

**Action on Screen**:
- Click the **"Flora"** button in the top navigation header.
- The 114-species Botanical Encyclopedia modal opens.
- Filter by **"Medicinal"** or type *"Neem"* or *"Tulsi"* into the search box.
- Click a plant card to reveal scientific taxonomy, vernacular names (Hindi, Bengali, Tamil), diagnostic traits, and ecological roles.

**Spoken Script**:
> *"WildSense includes a completely offline, SQLite-backed botanical encyclopedia of 114 native and regional species.
>
> If you're out in the field without cellular service, you have instant access to vernacular names across multiple Indian languages, diagnostic leaf and bark characteristics, ecological significance, and traditional Ayurvedic uses.
>
> Even better—every plant profile has a 'Start Mission' button to launch a physical investigation right from the field guide."*

---

### [1:45 – 2:20] Phase 4: Hands-Free Missions & Phone-Free Field Mode

**Action on Screen**:
- Close encyclopedia and view the generated mission: **"Leaf Detective"** or **"Texture Investigation"**.
- Click the **Audio Play** button: listen to the calm spoken audio instruction (via Browser Web Speech or ElevenLabs).
- Click **"Put Phone in Pocket & Start Exploring"**.
- Screen transitions into dark **Field Mode** with timer ticking.

**Spoken Script**:
> *"Instead of just identifying a name, WildSense generates a 2-minute physical observation mission adhering to our 10 Nature Mission Safety Rules—no damaging branches, no eating unknown plants, purely hands-on observation.
>
> To keep your eyes off the glass screen, WildSense speaks the mission aloud—either through high-fidelity ElevenLabs or 100% offline Browser Web Speech.
>
> Once spoken, you tap 'Put Phone in Pocket'. The screen dims into Field Mode. Your timer runs while your phone is safely in your pocket."*

---

### [2:20 – 2:45] Phase 5: Reflection, Grass Score & Local Journal

**Action on Screen**:
- Click **"Complete Mission"**.
- On the Reflection screen, type a brief sensory observation:  
  *e.g. "Veins were raised on the underside with a distinct fragrant aroma."*
- Click **"Submit Reflection & Calculate Score"**.
- View the **Grass Score** result card (e.g., **82 / 100** — *True Field Naturalist*).
- Click **"Journal"** in header to show the saved entry in local SQLite history.

**Spoken Script**:
> *"When you return, you log what your own human senses noticed. 
>
> WildSense then calculates the **Grass Score**—an explainable, anti-gamified 0 to 100 metric. 70% of the score comes strictly from your **World-to-Screen ratio**—rewarding you for spending minutes in the real world rather than in the app. 
>
> Everything is recorded into a private, local SQLite database on your device. Zero analytics, zero ad tracking."*

---

### [2:45 – 3:00] Phase 6: Architecture, Specialist Arbitration & Honest Limitations

**Action on Screen**:
- Show the header status badge: **"FastViT 4.2k ONNX • Offline AI • Zero Cloud"**.

**Spoken Script**:
> *"Under the hood, WildSense features a dual-model architecture. Our production release runs on the frozen 4,271-taxa FastViT global model. Behind a feature flag, we engineered a 7-class Indian Flora Specialist for regional plants like Neem, Tulsi, and Palash, protected by a 5-gate safety arbitrator.
>
> We believe in scientific honesty: Sweet Basil and Tulsi leaves look nearly identical without flowers, so our system marks them as 'Genus Confirmed' with explicit caveats. And because our specialist training dataset uses non-commercial research licenses, we do not claim commercial readiness—we present an ethical, open-source demonstration.
>
> WildSense is local, private, and designed to help humanity look closer, and then look away. Thank you!"*

---

## 🛠️ Demo Preparation Checklist

Before presenting live, perform these quick steps:

- [ ] Ensure backend is running in Terminal 1: `python backend/main.py`.
- [ ] Ensure frontend is running in Terminal 2: `npm run dev -- -H 0.0.0.0` (in `frontend/`).
- [ ] Open `http://localhost:3000` in your presentation browser.
- [ ] Verify audio is working: test your browser speakers.
- [ ] Keep `test_specimens/lotus.jpg` and `test_specimens/neem.jpg` easily accessible on your desktop or file picker.
- [ ] Reset demo state if needed (or simply click "Home" to start from the top).
