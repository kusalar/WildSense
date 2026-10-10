from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import random

class AIProvider(ABC):
    """Abstract base class for modular AI Providers (Ollama, Mock, etc.)"""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Name of the underlying AI model."""
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the AI provider is currently reachable."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, system: Optional[str] = None, format_json: bool = False) -> str:
        """Generate text from prompt."""
        pass


class MockProvider(AIProvider):
    """
    Fallback / offline demo provider when local Ollama is not running
    or during tests. Generates context-aware, safety-compliant nature missions and reflections.
    """

    def __init__(self, model_name: str = "mock-offline-ai"):
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    async def is_available(self) -> bool:
        return True

    async def generate(self, prompt: str, system: Optional[str] = None, format_json: bool = False) -> str:
        prompt_lower = prompt.lower()

        # Check if this is a reflection request
        if "reflect" in prompt_lower or "observation" in prompt_lower:
            return (
                "You stepped away from the screen and directly witnessed subtle details that cameras often flatten. "
                "Notice how the natural textures and light shifts reward patience. "
                "You didn't just label this specimen—you truly encountered it."
            )

        # Leaf / plant mission
        if "leaf" in prompt_lower or "plant" in prompt_lower:
            return """{
  "title": "Vein & Sunlight Detective",
  "instruction": "Don't pick the leaf. Crouch down and look underneath it against the ambient light. Spot three distinct differences between the top and bottom surfaces.",
  "estimated_minutes": 2,
  "physical_action": "Inspect the leaf from multiple angles without touching it.",
  "safety_note": "Do not touch or ingest unknown foliage. Observe gently from a respectful distance."
}"""

        # Tree mission
        if "tree" in prompt_lower:
            return """{
  "title": "Bark Texture Cartography",
  "instruction": "Step three paces back. Trace the deepest fissures in the bark with your eyes. Notice which direction the moss or lichen favors.",
  "estimated_minutes": 3,
  "physical_action": "Walk a half-circle around the trunk to see how shadows define its texture.",
  "safety_note": "Watch your footing for exposed roots and uneven ground."
}"""

        # Flower mission
        if "flower" in prompt_lower:
            return """{
  "title": "Pollinator Runway",
  "instruction": "Without disturbing the flower, find the central path or color gradients leading into its core. Count how many petals form its geometry.",
  "estimated_minutes": 2,
  "physical_action": "Lean in smoothly without brushing against petals or disturbing visiting insects.",
  "safety_note": "Keep hands clear of stinging pollinators."
}"""

        # Default nature object mission
        return """{
  "title": "Ground Truth Investigator",
  "instruction": "Step back two paces. Observe how this subject sits in its immediate micro-habitat. Find where it receives the most natural light.",
  "estimated_minutes": 2,
  "physical_action": "Shift your perspective 90 degrees and observe the contrast with surrounding soil or vegetation.",
  "safety_note": "Never touch, ingest, or disturb unknown wild organisms."
}"""
