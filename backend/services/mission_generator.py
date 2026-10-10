import json
import logging
import re
import time
from typing import Dict, Any, Optional
from services.ai_provider import AIProvider, MockProvider
from services.ollama_provider import OllamaProvider

logger = logging.getLogger("wildsense.mission")

SYSTEM_MISSION_PROMPT = """You are WildSense, an offline-first nature exploration companion.
Your goal is to get the user OFF the screen and physically observing the real living world.

CRITICAL SAFETY & QUALITY RULES:
1. NEVER instruct the user to eat, taste, chew, or ingest anything.
2. NEVER tell the user to pick leaves, break stems, snap branches, or damage flora.
3. NEVER tell the user to touch unknown plants, fungi, insects, or animals.
4. NEVER tell the user to approach wildlife, birds, nests, or burrows.
5. NEVER ask the user to enter dangerous terrain, steep slopes, or trespass.
6. The user puts their phone away in their pocket immediately. NEVER instruct the user to use, hold, tilt, or look at the phone. Observe directly with human eyes and body positioning.
7. Focus on: OBSERVE -> COMPARE -> LISTEN -> WALK -> NOTICE -> COUNT -> REFLECT.

You must return ONLY a valid JSON object with these exact keys:
{
  "title": "Short title (2-4 words)",
  "instruction": "Concrete real-world observation action (under 35 words)",
  "why": "Brief reason this detail is ecologically or physically interesting (under 25 words)",
  "estimated_minutes": 2,
  "physical_action": "Body positioning or movement (e.g. Crouch 2 paces back, walk half-circle)",
  "observation_goal": "Specific physical detail to find or count",
  "safety_note": "A clear safety reminder"
}
"""

SYSTEM_REFLECTION_PROMPT = """You are WildSense. The user just returned from a physical nature observation mission.
Validate their direct observation in a concise, calm naturalist tone.
Return ONLY a valid JSON object with these exact keys:
{
  "reflection": "2 short sentences acknowledging what they noticed.",
  "observation_highlight": "The specific physical detail they spotted.",
  "curiosity_fact": "One fascinating related biological/natural fact (under 25 words).",
  "next_suggestion": "One question to keep in mind for future walks."
}
"""

class MissionSafetyViolation(Exception):
    pass

class MissionGenerator:
    """
    Generates real-world nature observation missions adhering strictly to
    WildSense's 10 Touch Grass safety and interaction principles.
    """

    FORBIDDEN_PATTERNS = [
        r"(?<!don't\s)(?<!do not\s)(?<!without\s)(?<!never\s)(?<!or\s)(?<!nor\s)\b(eat|taste|ingest|chew|swallow|consume)\b",
        r"(?<!don't\s)(?<!do not\s)(?<!without\s)(?<!never\s)\b(pick|pluck|rip|tear off|break off|snap)\b",

        r"(?<!don't\s)(?<!do not\s)(?<!without\s)(?<!never\s)\b(touch\s+.*unknown|pet|handle\s+.*unknown|grab)\b",
        r"(?<!don't\s)(?<!do not\s)(?<!without\s)(?<!never\s)\b(catch|trap|hold|corner|chase)\b",
        r"(?<!don't\s)(?<!do not\s)(?<!without\s)(?<!never\s)\b(approach|disturb|bother)\s+.*(nest|hive|burrow|wildlife|fledgling|bird|animal)\b",
        r"(?<!don't\s)(?<!do not\s)(?<!without\s)(?<!never\s)\b(trespass|climb high|jump down|enter private)\b",
        r"\b(google|search online|look up on phone|photograph \d+ times)\b"
    ]

    CATEGORY_STRATEGIES = {
        "leaf": {
            "title": "Underside Architecture",
            "instruction": "Don't pick the leaf. Look underneath it and compare the veins, texture, and color with the upper surface.",
            "why": "The underside of a leaf often reveals vascular structures and stomata that are hidden from above.",
            "estimated_minutes": 2,
            "physical_action": "Crouch slightly and gently tilt your perspective without touching the blade.",
            "observation_goal": "Find three differences between the top and bottom surfaces.",
            "safety_note": "Observe without damaging, tearing, or removing the foliage."
        },
        "flower": {
            "title": "Floral Runway & Symmetry",
            "instruction": "Count the visible petals and notice whether they show radial or bilateral symmetry. Look for guidance lines leading toward the center.",
            "why": "Petal patterns act as ultraviolet landing strips for visiting native pollinators.",
            "estimated_minutes": 2,
            "physical_action": "Lean in smoothly at eye level with the blossom.",
            "observation_goal": "Count the petal count and identify which direction the bloom faces.",
            "safety_note": "Keep hands clear to give resting pollinators uninterrupted space."
        },
        "tree": {
            "title": "Bark Texture Cartography",
            "instruction": "Step back three paces. Trace the deepest fissures in the bark vertically. Notice which compass direction moss or lichen colonies favor.",
            "why": "Bark furrow depth and lichen colonization reflect prevailing moisture and microclimates.",
            "estimated_minutes": 3,
            "physical_action": "Walk a half-circle around the trunk to witness light and shadow play.",
            "observation_goal": "Identify the side of the trunk harboring the densest micro-growth.",
            "safety_note": "Watch your footing for exposed roots and uneven trail soil."
        },
        "rock": {
            "title": "Mineral Contrast & Fissures",
            "instruction": "Look closely at the rock surface without disturbing it. Find how many color shades or mineral flecks make up its visible face.",
            "why": "Multi-toned speckles indicate crystalline cooling rates and weathering history.",
            "estimated_minutes": 2,
            "physical_action": "Shift your perspective 90 degrees to see how ambient light catches mineral facets.",
            "observation_goal": "Spot two distinct textures: weathered versus protected crevices.",
            "safety_note": "Do not overturn heavy stones or disturb organisms sheltering beneath."
        },
        "insect": {
            "title": "Patience & Micro-Pacing",
            "instruction": "Remain still 3 paces away. Watch its direction of travel and cadence without moving closer or casting a sudden shadow.",
            "why": "Invertebrates adjust foraging cadence based on micro-vibrations and thermal patches.",
            "estimated_minutes": 2,
            "physical_action": "Freeze in place and observe motion against the background substrate.",
            "observation_goal": "Count how many seconds it pauses between locomotion bursts.",
            "safety_note": "Never touch, trap, or disturb insects or their pathways."
        },
        "bird": {
            "title": "Acoustic & Perch Tracking",
            "instruction": "Lower your gaze and listen before looking up. Track the direction of its vocalization or wing fluttering without stepping toward it.",
            "why": "Bird song patterns repeat in territorial rhythms that are easier to isolate with eyes softened.",
            "estimated_minutes": 3,
            "physical_action": "Stand completely still with shoulders relaxed and ears attuned.",
            "observation_goal": "Count how many intervals occur between vocal calls.",
            "safety_note": "Never approach active nests, fledglings, or roosting branches."
        },
        "fungus": {
            "title": "Shelf & Spore Geometry",
            "instruction": "Look at the underside of the fruiting body without touching it. Observe whether it features gills, pores, or a smooth wooden shelf.",
            "why": "Underside spore release mechanisms distinguish polypores from agaric fungi.",
            "estimated_minutes": 2,
            "physical_action": "Kneel beside the substrate without making contact with the organism.",
            "observation_goal": "Identify if spore surface is pitted, ribbed, or smooth.",
            "safety_note": "NEVER touch or ingest wild fungi. Observe strictly from a distance."
        },
        "plant": {
            "title": "Foliage Node Investigator",
            "instruction": "Trace the stem upwards with your eyes. Observe whether leaves emerge opposite each other in pairs or alternate in a spiral.",
            "why": "Phyllotaxy (leaf arrangement) optimizes solar absorption and rainfall drainage.",
            "estimated_minutes": 2,
            "physical_action": "Step side-to-side to view the stem silhouette against the light.",
            "observation_goal": "Determine if the leaf pattern is opposite, alternate, or whorled.",
            "safety_note": "Do not touch unidentified wild plants or ingest any botanical matter."
        },
        "other": {
            "title": "Real-World Ground Truth",
            "instruction": "Step back two paces. Find one physical detail of this specimen that would have been completely missed in a flat photograph.",
            "why": "Physical presence reveals depth, shadow transitions, and ambient micro-habitat.",
            "estimated_minutes": 2,
            "physical_action": "Walk slowly around the perimeter of the specimen.",
            "observation_goal": "Notice the relationship between the object and its immediate surroundings.",
            "safety_note": "Always respect wild habitats and maintain distance from unknown organisms."
        }
    }

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        self.ai_provider = ai_provider or OllamaProvider()
        self.mock_provider = MockProvider()

    def validate_safety(self, mission: Dict[str, Any]) -> bool:
        """Verify that mission contains zero unsafe or destructive suggestions."""
        combined_text = f"{mission.get('title', '')} {mission.get('instruction', '')} {mission.get('physical_action', '')}".lower()
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, combined_text):
                logger.warning(f"Safety violation triggered by pattern: {pattern}")
                return False
        return True

    def get_fallback_mission(self, category: str, object_name: str) -> Dict[str, Any]:
        """Category-specific robust fallback mission."""
        cat_key = category.lower() if category and category.lower() in self.CATEGORY_STRATEGIES else "other"
        base = dict(self.CATEGORY_STRATEGIES[cat_key])
        if object_name and "unknown" not in object_name.lower():
            base["instruction"] = f"Observing this {object_name}: {base['instruction']}"
        return base

    async def generate_mission(
        self,
        object_name: str,
        category: str,
        confidence: float = 0.74,
        difficulty: str = "normal",
        available_time_minutes: int = 2,
        context: Optional[str] = None,
        description: Optional[str] = None,
        uncertainty: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a structured, safe, phone-free observation mission."""
        cat_clean = category.lower() if category else "other"
        strat_hint = self.CATEGORY_STRATEGIES.get(cat_clean, self.CATEGORY_STRATEGIES["other"])

        # Model-agnostic mission prompt including all constraints
        prompt = f"""Specimen: {object_name}
Category: {category}
Visual Confidence: {confidence:.2f}
Description: {description or 'Natural field specimen'}
Uncertainty: {uncertainty or 'Visual identification is approximate'}
Target Duration: {available_time_minutes} minutes
Suggested Natural Focus: {strat_hint['observation_goal']}

MANDATORY RULES:
- The user must perform a concrete physical movement or perspective shift (e.g. crouch, step back, tilt perspective, listen).
- The user must be able to put their phone away. Zero phone interaction during exploration.
- Never suggest touching or ingesting unknown species.
- Never suggest damaging plants, breaking branches, or disturbing wildlife/nests.
- Never suggest trespassing or steep terrain.

Generate a safe, phone-free observation mission in valid JSON format."""

        # Attempt local model generation
        start_time = time.perf_counter()
        try:
            if await self.ai_provider.is_available():
                # Pass format_json=True if supported by provider
                try:
                    raw = await self.ai_provider.generate(prompt=prompt, system=SYSTEM_MISSION_PROMPT, format_json=True)
                except TypeError:
                    raw = await self.ai_provider.generate(prompt=prompt, system=SYSTEM_MISSION_PROMPT)

                parsed = self._parse_json_mission(raw)
                elapsed_ms = int((time.perf_counter() - start_time) * 1000)
                if parsed and self.validate_safety(parsed):
                    parsed["estimated_minutes"] = available_time_minutes
                    parsed["llm_inference_ms"] = elapsed_ms
                    provider_type = "ollama" if "ollama" in str(type(self.ai_provider)).lower() else "local_llm"
                    parsed["provider"] = provider_type
                    parsed["model"] = getattr(self.ai_provider, "model_name", "local_llm")
                    return parsed
                else:
                    logger.warning("LLM mission failed validation or safety check. Using fallback strategy.")
        except Exception as e:
            logger.warning(f"Local AI mission generation failed: {e}. Using strategy fallback.")

        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        # Return guaranteed safe strategy mission
        fallback = self.get_fallback_mission(category, object_name)
        fallback["llm_inference_ms"] = elapsed_ms
        fallback["provider"] = "rule_strategy_fallback"
        fallback["model"] = getattr(self.ai_provider, "model_name", "strategy_fallback")
        return fallback

    async def generate_reflection(
        self,
        object_name: str,
        category: str,
        mission_title: str,
        user_observation: str,
        field_time_seconds: int
    ) -> Dict[str, Any]:
        """
        Generates structured AI reflection:
        reflection, observation_highlight, curiosity_fact, next_suggestion
        """
        obs_clean = user_observation.strip() if user_observation else ""

        if not obs_clean:
            return {
                "reflection": f"You dedicated {field_time_seconds} seconds of quiet immersion to the living world instead of looking at a screen.",
                "observation_highlight": "Uninterrupted physical presence in nature.",
                "curiosity_fact": "Even brief periods of open-air stillness measurably lower physiological stress markers.",
                "next_suggestion": "Next time, pause to note the direction of the breeze before beginning."
            }

        prompt = f"""Specimen: {object_name} ({category})
Mission: {mission_title}
Time in Field: {field_time_seconds} seconds
User's Real-World Observation: "{obs_clean}"

Generate a short 2-sentence reflection acknowledging this specific observation, one curiosity fact, and one future suggestion."""

        try:
            if await self.ai_provider.is_available():
                raw = await self.ai_provider.generate(prompt=prompt, system=SYSTEM_REFLECTION_PROMPT)
                parsed = self._parse_json_reflection(raw)
                if parsed:
                    return parsed
        except Exception as e:
            logger.warning(f"Reflection generation fallback: {e}")

        # Deterministic fallback reflection
        return {
            "reflection": f"You noticed that {obs_clean.lower() if not obs_clean.endswith('.') else obs_clean}. You investigated real physical characteristics that cameras compress.",
            "observation_highlight": obs_clean[:60] + ("..." if len(obs_clean) > 60 else ""),
            "curiosity_fact": f"Natural organisms in the {category} kingdom adapt surface traits specifically for moisture retention and light capture.",
            "next_suggestion": "Next time, compare two specimens side-by-side without disturbing either."
        }

    def _parse_json_mission(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse structured mission from LLM response, handling markdown fences and JSON repair."""
        try:
            clean_text = text
            fence_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
            if fence_match:
                clean_text = fence_match.group(1)

            json_match = re.search(r"\{[\s\S]*\}", clean_text)
            if json_match:
                data = json.loads(json_match.group(0))
                if isinstance(data, dict) and "title" in data and "instruction" in data:
                    data.setdefault("why", "Direct observation reveals details obscured by digital screens.")
                    data.setdefault("estimated_minutes", 2)
                    data.setdefault("physical_action", "Observe from multiple perspectives.")
                    data.setdefault("observation_goal", "Find physical distinguishing marks.")
                    data.setdefault("safety_note", "Do not touch unknown plants or disturb wildlife.")
                    return data
        except Exception as e:
            logger.debug(f"JSON parse error: {e}")
        return None

    def _parse_json_reflection(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse structured reflection from LLM response."""
        try:
            json_match = re.search(r"\{[\s\S]*\}", text)
            if json_match:
                data = json.loads(json_match.group(0))
                if "reflection" in data:
                    data.setdefault("observation_highlight", "Direct physical detail.")
                    data.setdefault("curiosity_fact", "Nature rewards patience and close sensory attention.")
                    data.setdefault("next_suggestion", "Compare this specimen with another nearby on your next walk.")
                    return data
        except Exception:
            pass
        return None
