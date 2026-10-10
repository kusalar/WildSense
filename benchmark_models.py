"""
WildSense - Model Benchmark Suite (Task 5)
Compares Qwen3 4B vs Google Gemma 2 2B as local reasoning engines.

Deterministic Rubric (5 Points Max):
- Schema valid: 1 point (all 7 required fields present, valid types)
- Safety valid: 1 point (zero forbidden safety patterns)
- Physical action present: 1 point (concrete movement or body perspective)
- Observation goal present: 1 point (clear sensory/observational target)
- Phone-away compatible: 1 point (zero phone/screen/camera dependency)
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

try:
    from services.ollama_provider import OllamaProvider
    from services.mission_generator import MissionGenerator, SYSTEM_MISSION_PROMPT
    import config
except ImportError:
    from backend.services.ollama_provider import OllamaProvider  # type: ignore
    from backend.services.mission_generator import MissionGenerator, SYSTEM_MISSION_PROMPT  # type: ignore
    from backend import config  # type: ignore

TEST_SPECIMENS: List[Dict[str, Any]] = [
    {
        "id": "leaf",
        "name": "Neem Leaf (Azadirachta indica)",
        "category": "leaf",
        "confidence": 0.88,
        "description": "Serrated green leaflet with visible pinnate veins and curved tip.",
        "uncertainty": "Botanical family confirmed; specimen shows healthy green foliage."
    },
    {
        "id": "flower",
        "name": "Wild Asteraceae Blossom",
        "category": "flower",
        "confidence": 0.82,
        "description": "Yellow composite blossom with radial disc florets in open sun.",
        "uncertainty": "Common wild sunflower relative; petal count varies."
    },
    {
        "id": "rock",
        "name": "Weathered Basalt Stone",
        "category": "rock",
        "confidence": 0.91,
        "description": "Dark grey surface stone with mineral flecks, fissures, and partial lichen.",
        "uncertainty": "Inert geological formation; weathering patterns evident."
    },
    {
        "id": "tree",
        "name": "Mature Bark Trunk",
        "category": "tree",
        "confidence": 0.85,
        "description": "Thick furrowed tree bark with north-facing moss growth and deep fissures.",
        "uncertainty": "Perennial woodland trunk; bark ridges provide micro-habitats."
    },
    {
        "id": "unknown_plant",
        "name": "Unidentified Forest Understory Plant",
        "category": "plant",
        "confidence": 0.52,
        "description": "Low-growing herbaceous vegetation with ovate leaves in partial shade.",
        "uncertainty": "Uncertain botanical species; do not handle or touch."
    }
]

PHONE_FORBIDDEN_WORDS = ["phone", "screen", "camera", "photo", "photograph", "app", "take a picture", "snap a picture", "record on"]

PHYSICAL_ACTION_KEYWORDS = ["crouch", "step", "walk", "tilt", "turn", "look", "lean", "stand", "shift", "pace", "kneel", "freeze", "position", "move", "eye level", "distance", "angle", "back", "circle"]

OBSERVATION_KEYWORDS = ["count", "find", "spot", "notice", "compare", "identify", "observe", "detail", "color", "texture", "difference", "shape", "ridges", "veins", "pattern"]

REQUIRED_FIELDS = ["title", "instruction", "why", "estimated_minutes", "physical_action", "observation_goal", "safety_note"]


def evaluate_mission(raw_text: str, generator: MissionGenerator) -> Tuple[float, Dict[str, Any], Dict[str, bool]]:
    """
    Deterministically evaluates a raw model completion against the 5-point quality rubric.
    """
    scores = {
        "schema_valid": False,
        "safety_valid": False,
        "physical_action_present": False,
        "observation_goal_present": False,
        "phone_away_compatible": False
    }

    parsed = generator._parse_json_mission(raw_text)

    # 1. Schema valid (1 pt)
    if parsed and isinstance(parsed, dict):
        has_all_fields = all(k in parsed and parsed[k] is not None for k in REQUIRED_FIELDS)
        if has_all_fields and isinstance(parsed.get("title"), str) and len(parsed["title"].strip()) > 0:
            scores["schema_valid"] = True
    else:
        parsed = {}

    # 2. Safety valid (1 pt)
    if parsed and generator.validate_safety(parsed):
        scores["safety_valid"] = True

    # 3. Physical action present (1 pt)
    act = str(parsed.get("physical_action", "")).lower()
    if len(act) >= 8 and any(kw in act for kw in PHYSICAL_ACTION_KEYWORDS):
        scores["physical_action_present"] = True

    # 4. Observation goal present (1 pt)
    goal = str(parsed.get("observation_goal", "")).lower()
    if len(goal) >= 8 and any(kw in goal for kw in OBSERVATION_KEYWORDS):
        scores["observation_goal_present"] = True

    # 5. Phone-away compatible (1 pt)
    full_text = f"{parsed.get('instruction', '')} {parsed.get('physical_action', '')} {parsed.get('observation_goal', '')}".lower()
    if not any(fw in full_text for fw in PHONE_FORBIDDEN_WORDS):
        scores["phone_away_compatible"] = True

    total = sum(1.0 for v in scores.values() if v)
    return total, parsed, scores


async def benchmark_model(model_name: str, provider: OllamaProvider, generator: MissionGenerator) -> Dict[str, Any]:
    print(f"\n=======================================================")
    print(f"  BENCHMARKING MODEL: {model_name}")
    print(f"=======================================================")

    provider.set_model(model_name)
    results = []
    total_latency_ms = 0

    for idx, spec in enumerate(TEST_SPECIMENS, 1):
        print(f"\n[{idx}/5] Testing Case: {str(spec['id']).upper()} ({spec['name']})...")

        prompt = f"""Specimen: {spec['name']}
Category: {spec['category']}
Visual Confidence: {spec['confidence']:.2f}
Description: {spec['description']}
Uncertainty: {spec['uncertainty']}
Target Duration: 2 minutes
Suggested Natural Focus: Notice surface patterns and texture

MANDATORY RULES:
- The user must perform a concrete physical movement or perspective shift (e.g. crouch, step back, tilt perspective, listen).
- The user must be able to put their phone away. Zero phone interaction during exploration.
- Never suggest touching or ingesting unknown species.
- Never suggest damaging plants, breaking branches, or disturbing wildlife/nests.
- Never suggest trespassing or steep terrain.

Generate a safe, phone-free observation mission in valid JSON format."""

        start = time.perf_counter()
        try:
            raw = await provider.generate(prompt=prompt, system=SYSTEM_MISSION_PROMPT, format_json=True)
            latency_ms = int((time.perf_counter() - start) * 1000)
            total_latency_ms += latency_ms

            score, parsed, rubric = evaluate_mission(raw, generator)

            token_estimate = len(raw.split()) if raw else 0

            print(f"  -> Latency: {latency_ms} ms | Score: {score}/5.0 | Tokens: ~{token_estimate}")
            print(f"  -> Title: \"{parsed.get('title', 'N/A')}\"")
            print(f"  -> Action: \"{parsed.get('physical_action', 'N/A')}\"")
            print(f"  -> Rubric: Schema={rubric['schema_valid']}, Safety={rubric['safety_valid']}, Action={rubric['physical_action_present']}, Goal={rubric['observation_goal_present']}, PhoneAway={rubric['phone_away_compatible']}")

            results.append({
                "case": spec["id"],
                "specimen": spec["name"],
                "latency_ms": latency_ms,
                "score": score,
                "rubric": rubric,
                "tokens": token_estimate,
                "mission": parsed,
                "raw_preview": raw[:120] + "..." if len(raw) > 120 else raw
            })
        except Exception as e:
            latency_ms = int((time.perf_counter() - start) * 1000)
            print(f"  -> ERROR during inference: {e}")
            results.append({
                "case": spec["id"],
                "specimen": spec["name"],
                "latency_ms": latency_ms,
                "score": 0.0,
                "rubric": {},
                "tokens": 0,
                "error": str(e)
            })

    avg_latency = total_latency_ms / len(results) if results else 0
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0

    return {
        "model": model_name,
        "cases_tested": len(results),
        "avg_latency_ms": avg_latency,
        "avg_score": avg_score,
        "results": results
    }


async def main():
    print("=" * 60)
    print("  WILDSENSE LOCAL REASONING BENCHMARK (Task 5)")
    print("  Comparing Qwen3 4B vs Google Gemma 2 2B")
    print("=" * 60)

    ollama = OllamaProvider(base_url=config.OLLAMA_BASE_URL, model=config.REASONING_MODEL)
    is_avail = await ollama.is_available()

    if not is_avail:
        print(f"ERROR: Ollama is not accessible at {config.OLLAMA_BASE_URL}!")
        return

    models_info = await ollama.list_models()
    print(f"Installed Ollama models: {models_info}")

    qwen_model = "qwen3:4b"
    gemma_model = config.GEMMA_MODEL or "gemma2:2b"

    generator = MissionGenerator(ai_provider=ollama)

    # 1. Benchmark Qwen
    qwen_report = await benchmark_model(qwen_model, ollama, generator)

    # 2. Benchmark Gemma
    gemma_report = await benchmark_model(gemma_model, ollama, generator)

    print("\n" + "=" * 60)
    print("               FINAL BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"Model: {qwen_report['model']}")
    print(f"  - Average Score:   {qwen_report['avg_score']:.2f} / 5.0")
    print(f"  - Average Latency: {qwen_report['avg_latency_ms']:.0f} ms ({qwen_report['avg_latency_ms']/1000:.2f}s)")
    print("-" * 60)
    print(f"Model: {gemma_report['model']}")
    print(f"  - Average Score:   {gemma_report['avg_score']:.2f} / 5.0")
    print(f"  - Average Latency: {gemma_report['avg_latency_ms']:.0f} ms ({gemma_report['avg_latency_ms']/1000:.2f}s)")
    print("=" * 60)

    # Save benchmark results to JSON file
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "qwen": qwen_report,
        "gemma": gemma_report
    }
    with open("benchmark_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\nBenchmark results saved to benchmark_results.json")


if __name__ == "__main__":
    asyncio.run(main())
