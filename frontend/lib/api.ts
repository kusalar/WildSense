const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export interface HealthStatus {
  status: string;
  ollama_connected: boolean;
  configured_model: string;
  reasoning_model?: string;
  vision_model: string;
  vision_available: boolean;
  available_models: string[];
  mode: string;
}

export interface RecognizeResult {
  category: string;
  common_name: string;
  confidence: number;
  description: string;
  uncertainty: string;
  inference_ms?: number;
  provider?: string;
}

export interface MissionResult {
  title: string;
  instruction: string;
  why: string;
  estimated_minutes: number;
  physical_action: string;
  observation_goal: string;
  safety_note: string;
  llm_inference_ms?: number;
  provider?: string;
  model?: string;
}

export interface ReflectionDetails {
  reflection: string;
  observation_highlight: string;
  curiosity_fact: string;
  next_suggestion: string;
}

export interface ScoreBreakdown {
  ratio_points: number;
  mission_points: number;
  field_time_points: number;
  reflection_points: number;
  max_ratio_points?: number;
  max_mission_points?: number;
  max_field_time_points?: number;
  max_reflection_points?: number;
}

export interface ScoreMetrics {
  world_time_seconds: number;
  screen_time_seconds: number;
  world_screen_ratio: number;
  mission_completed: boolean;
  phone_free_seconds: number;
  reflection_completed: boolean;
}

export interface GrassScoreResult {
  score?: number;
  grass_score: number;
  breakdown?: ScoreBreakdown;
  metrics?: ScoreMetrics;
  screen_time_seconds: number;
  field_time_seconds: number;
  screen_time_formatted: string;
  field_time_formatted: string;
  ratio: number;
  ratio_formatted: string;
  verdict: string;
  explanation?: string;
}

export interface AudioNarration {
  status: string;
  provider: string;
  text: string;
  duration_seconds: number;
  supports_client_speech: boolean;
  audio_url?: string | null;
  audio_base64?: string | null;
  speech_rate: number;
  pitch: number;
  voice_id?: string | null;
  model?: string | null;
  fallback_reason?: string | null;
}

export interface AudioStatus {
  configured_provider: string;
  active_provider: string;
  elevenlabs_configured: boolean;
  voice_id?: string | null;
  model_id?: string | null;
  browser_speech_supported: boolean;
  mode: string;
}


export interface JournalEntry {
  id: string;
  created_at: string;
  completed_at?: string;
  object_name: string;
  category: string;
  confidence: number;
  uncertainty?: string;
  mission_title?: string;
  mission_instruction?: string;
  mission_why?: string;
  observation_goal?: string;
  screen_time_seconds: number;
  field_time_seconds: number;
  grass_score: number;
  ratio: number;
  user_observation?: string;
  ai_reflection?: string;
  curiosity_fact?: string;
  next_suggestion?: string;
}

export async function fetchHealth(): Promise<HealthStatus> {
  try {
    const res = await fetch(`${API_BASE.replace('/api', '')}/health`, { cache: "no-store" });
    if (!res.ok) throw new Error("Health check failed");
    return await res.json();
  } catch (err) {
    return {
      status: "degraded",
      ollama_connected: false,
      configured_model: "fallback-mock",
      vision_model: "local_cv_fallback",
      vision_available: false,
      available_models: [],
      mode: "browser_local"
    };
  }
}

export async function fetchPresets(): Promise<Record<string, RecognizeResult>> {
  try {
    const res = await fetch(`${API_BASE}/presets`);
    if (!res.ok) throw new Error("Presets fetch failed");
    return await res.json();
  } catch {
    return {
      demo_leaf: {
        category: "leaf",
        common_name: "Likely Neem Leaf",
        confidence: 0.74,
        description: "Elongated serrated pinnate leaflet with curved tip.",
        uncertainty: "Visual identification is approximate.",
        provider: "demo_preset",
        inference_ms: 10
      },
      demo_flower: {
        category: "flower",
        common_name: "Wild Field Flower",
        confidence: 0.78,
        description: "Bright radial golden inflorescence composed of composite florets.",
        uncertainty: "Radial petal symmetry suggests wild Asteraceae.",
        provider: "demo_preset",
        inference_ms: 10
      },
      demo_rock: {
        category: "rock",
        common_name: "Weathered Surface Rock",
        confidence: 0.81,
        description: "Coarse-grained weathered mineral surface with lichen rings.",
        uncertainty: "Mineral morphology suggests granite or fieldstone.",
        provider: "demo_preset",
        inference_ms: 10
      },
      demo_tree: {
        category: "tree",
        common_name: "Mature Bark Trunk",
        confidence: 0.76,
        description: "Deeply fissured woody bark showing vertical ridges.",
        uncertainty: "Bark patterns indicate mature deciduous trunk.",
        provider: "demo_preset",
        inference_ms: 10
      },
      demo_unknown_plant: {
        category: "plant",
        common_name: "Unidentified Understory Plant",
        confidence: 0.58,
        description: "Compact herbaceous understory growth.",
        uncertainty: "Low confidence match; specimen partially occluded.",
        provider: "demo_preset",
        inference_ms: 10
      }
    };
  }
}

export type RecognizeInput =
  | { imageFile?: File | null; imageBase64?: string | null; presetId?: string | null }
  | File
  | string;

export async function recognizeObject(
  param1?: RecognizeInput | null,
  param2?: string | null
): Promise<RecognizeResult> {
  let imageFile: File | null = null;
  let imageBase64: string | null = null;
  let presetId: string | null = null;

  if (param1 instanceof File) {
    imageFile = param1;
    if (param2) presetId = param2;
  } else if (typeof param1 === "string") {
    if (param1.startsWith("data:") || param1.length > 80) {
      imageBase64 = param1;
    } else {
      presetId = param1;
    }
    if (param2) presetId = param2;
  } else if (param1 && typeof param1 === "object") {
    imageFile = param1.imageFile || null;
    imageBase64 = param1.imageBase64 || null;
    presetId = param1.presetId || null;
  }

  try {
    // 1. If real image file uploaded, send via multipart/form-data
    if (imageFile) {
      const formData = new FormData();
      formData.append("image", imageFile);
      if (presetId) formData.append("preset_id", presetId);
      const res = await fetch(`${API_BASE}/recognize`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Multipart recognition failed");
      return await res.json();
    }

    // 2. Otherwise send JSON payload
    const res = await fetch(`${API_BASE}/recognize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_base64: imageBase64, preset_id: presetId }),
    });
    if (!res.ok) throw new Error("Recognition failed");
    return await res.json();
  } catch {
    // Local fallback
    if (presetId === "demo_flower") {
      return {
        category: "flower",
        common_name: "Wild Field Flower",
        confidence: 0.78,
        description: "Bright radial golden inflorescence with composite florets.",
        uncertainty: "Radial petal symmetry suggests wild Asteraceae.",
        provider: "client_fallback",
        inference_ms: 15
      };
    }
    if (presetId === "demo_rock") {
      return {
        category: "rock",
        common_name: "Weathered Surface Rock",
        confidence: 0.81,
        description: "Coarse-grained weathered mineral surface with micro-lichen rings.",
        uncertainty: "Mineral morphology suggests fieldstone.",
        provider: "client_fallback",
        inference_ms: 15
      };
    }
    if (presetId === "demo_tree") {
      return {
        category: "tree",
        common_name: "Mature Bark Trunk",
        confidence: 0.76,
        description: "Deeply fissured woody bark showing vertical ridges.",
        uncertainty: "Bark patterns indicate mature deciduous trunk.",
        provider: "client_fallback",
        inference_ms: 15
      };
    }
    if (presetId === "demo_unknown_plant") {
      return {
        category: "plant",
        common_name: "Unidentified Understory Plant",
        confidence: 0.58,
        description: "Compact herbaceous understory growth with alternating blade clusters.",
        uncertainty: "Low confidence match; specimen details partially occluded.",
        provider: "client_fallback",
        inference_ms: 15
      };
    }
    return {
      category: "leaf",
      common_name: "Likely Neem Leaf",
      confidence: 0.74,
      description: "Elongated serrated pinnate leaflet with distinct curved tip and light underside veins.",
      uncertainty: "Visual identification is approximate; vein angles match Azadirachta genus.",
      provider: "client_fallback",
      inference_ms: 15
    };
  }
}

export async function createMission(params: {
  object_name: string;
  category: string;
  confidence?: number;
  sessionId?: string;
}): Promise<MissionResult> {
  try {
    const res = await fetch(`${API_BASE}/mission`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        object_name: params.object_name,
        category: params.category,
        confidence: params.confidence || 0.74,
        session_id: params.sessionId
      }),
    });
    if (!res.ok) throw new Error("Mission generation failed");
    return await res.json();
  } catch {
    return {
      title: "Underside Architecture",
      instruction: "Don't pick the leaf. Look underneath it and compare the veins, texture, and color with the upper surface.",
      why: "The underside of a leaf often reveals vascular structures and stomata that are hidden from above.",
      estimated_minutes: 2,
      physical_action: "Crouch slightly and gently tilt your perspective without touching the blade.",
      observation_goal: "Find three differences between the top and bottom surfaces.",
      safety_note: "Observe without damaging, tearing, or removing the foliage."
    };
  }
}

export interface AudioRequestParams {
  text?: string;
  title?: string;
  instruction?: string;
  physical_action?: string;
  observation_goal?: string;
  safety_note?: string;
  estimated_minutes?: number;
  provider?: string;
}

export async function fetchAudioStatus(): Promise<AudioStatus> {
  try {
    const res = await fetch(`${API_BASE}/audio/status`);
    if (!res.ok) throw new Error("Audio status request failed");
    return await res.json();
  } catch {
    return {
      configured_provider: "browser",
      active_provider: "browser",
      elevenlabs_configured: false,
      browser_speech_supported: true,
      mode: "local_browser_speech"
    };
  }
}

export async function fetchAudioNarration(
  params: string | AudioRequestParams,
  preferredProvider?: string
): Promise<AudioNarration> {
  const payload = typeof params === "string"
    ? { text: params, provider: preferredProvider }
    : { ...params, provider: preferredProvider || params.provider };

  try {
    const res = await fetch(`${API_BASE}/audio`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Audio synthesis request failed");
    return await res.json();
  } catch (err: any) {
    const fallbackText = typeof params === "string" ? params : (params.text || params.title || "Observation Mission");
    return {
      status: "client_fallback",
      provider: "browser",
      text: fallbackText,
      duration_seconds: 5.0,
      supports_client_speech: true,
      audio_url: null,
      speech_rate: 0.92,
      pitch: 0.95,
      fallback_reason: "Network request failed; local browser speech fallback active"
    };
  }
}


export async function createSession(params: {
  object_name: string;
  category: string;
  confidence?: number;
  uncertainty?: string;
  description?: string;
}): Promise<{ id: string }> {
  try {
    const res = await fetch(`${API_BASE}/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error("Session create failed");
    return await res.json();
  } catch {
    return { id: "offline-" + Date.now() };
  }
}

export async function completeSession(sessionId: string, params: {
  screen_time_seconds: number;
  field_time_seconds: number;
  user_observation?: string;
}): Promise<{
  id: string;
  grass_score: GrassScoreResult;
  reflection_details?: ReflectionDetails;
  ai_reflection?: string;
}> {
  try {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/complete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error("Complete session failed");
    return await res.json();
  } catch {
    const worldSec = params.field_time_seconds;
    const screenSec = Math.max(1, params.screen_time_seconds);
    const ratio = Math.round((worldSec / screenSec) * 100) / 100;
    const obs = (params.user_observation || "").trim();

    // Piecewise ratio calculation
    const ratioKnots: [number, number][] = [
      [0.0, 0.0], [1.0, 25.0], [2.0, 40.0], [3.0, 55.0], [4.0, 63.0], [5.0, 70.0], [7.0, 79.0], [10.0, 90.0], [20.0, 100.0]
    ];
    let baseRatio = 100.0;
    if (ratio <= 0) baseRatio = 0.0;
    else if (ratio < 20) {
      for (let i = 0; i < ratioKnots.length - 1; i++) {
        const [x0, y0] = ratioKnots[i];
        const [x1, y1] = ratioKnots[i + 1];
        if (ratio >= x0 && ratio <= x1) {
          baseRatio = y0 + ((ratio - x0) / (x1 - x0)) * (y1 - y0);
          break;
        }
      }
    }
    const ratioPoints = Math.round(baseRatio * 0.70);
    const missionPoints = 15;

    // Field time knots
    const fieldKnots: [number, number][] = [
      [0, 0], [30, 3], [60, 5], [120, 7], [300, 8.5], [600, 10]
    ];
    let fieldPointsRaw = 10.0;
    if (worldSec <= 0) fieldPointsRaw = 0.0;
    else if (worldSec < 600) {
      for (let i = 0; i < fieldKnots.length - 1; i++) {
        const [x0, y0] = fieldKnots[i];
        const [x1, y1] = fieldKnots[i + 1];
        if (worldSec >= x0 && worldSec <= x1) {
          fieldPointsRaw = y0 + ((worldSec - x0) / (x1 - x0)) * (y1 - y0);
          break;
        }
      }
    }
    const fieldTimePoints = Math.round(fieldPointsRaw);

    let reflectionPoints = 0;
    if (!obs) {
      reflectionPoints = 0;
    } else if (obs.length < 15) {
      reflectionPoints = 2;
    } else {
      const hasCuriosity = /[?]|why|wonder|how|curious|notice|noticed|what/i.test(obs);
      reflectionPoints = hasCuriosity ? 5 : 4;
    }

    const finalScore = Math.max(0, Math.min(100, ratioPoints + missionPoints + fieldTimePoints + reflectionPoints));

    return {
      id: sessionId,
      grass_score: {
        score: finalScore,
        grass_score: finalScore,
        screen_time_seconds: params.screen_time_seconds,
        field_time_seconds: params.field_time_seconds,
        screen_time_formatted: `${params.screen_time_seconds}s`,
        field_time_formatted: `${Math.floor(params.field_time_seconds / 60)}m ${params.field_time_seconds % 60}s`,
        ratio,
        ratio_formatted: `${ratio}×`,
        verdict: finalScore >= 80 ? "True Field Naturalist 🌿" : "Dedicated Observer 🍃",
        explanation: `You spent ${ratio}× more time exploring than looking at your screen.`,
        breakdown: {
          ratio_points: ratioPoints,
          mission_points: missionPoints,
          field_time_points: fieldTimePoints,
          reflection_points: reflectionPoints,
          max_ratio_points: 70,
          max_mission_points: 15,
          max_field_time_points: 10,
          max_reflection_points: 5,
        },
        metrics: {
          world_time_seconds: worldSec,
          screen_time_seconds: screenSec,
          world_screen_ratio: ratio,
          mission_completed: true,
          phone_free_seconds: worldSec,
          reflection_completed: obs.length > 0,
        }
      },
      reflection_details: {
        reflection: obs
          ? `You noticed "${obs}". You investigated real physical characteristics that cameras compress.`
          : "You dedicated your full focus to the living world instead of looking at a screen.",
        observation_highlight: obs ? obs.slice(0, 50) : "Physical stillness",
        curiosity_fact: "Light angle shifts alter apparent vein relief and leaf pigmentation.",
        next_suggestion: "Compare two leaves from the same plant on your next walk."
      },
      ai_reflection: obs
        ? `You noticed "${obs}". You didn't just look up an image on a phone—you took time to physically observe and investigate the real specimen.`
        : "You stepped away from the screen and gave your full focus to the living world."
    };
  }
}

export async function fetchJournal(): Promise<JournalEntry[]> {
  try {
    const res = await fetch(`${API_BASE}/journal`);
    if (!res.ok) throw new Error("Journal fetch failed");
    return await res.json();
  } catch {
    return [];
  }
}

export async function selectModel(model: string): Promise<{ status: string; active_model: string }> {
  try {
    const res = await fetch(`${API_BASE}/models/select`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model })
    });
    if (!res.ok) throw new Error("Model selection failed");
    return await res.json();
  } catch {
    return { status: "local", active_model: model };
  }
}
