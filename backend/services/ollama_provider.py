import json
import logging
from typing import Optional, List, Dict, Any
import httpx
from services.ai_provider import AIProvider
from config import OLLAMA_BASE_URL, DEFAULT_MODEL

logger = logging.getLogger("wildsense.ollama")

class OllamaProvider(AIProvider):
    """
    Communicates directly with the local Ollama daemon.
    Zero cloud dependencies; 100% private and offline.
    """

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = DEFAULT_MODEL, timeout_seconds: float = 90.0):
        self.base_url = base_url.rstrip("/")
        self._model_name = model
        self.timeout = timeout_seconds

    @property
    def model_name(self) -> str:
        return self._model_name

    def set_model(self, model: str):
        self._model_name = model

    async def is_available(self) -> bool:
        """Ping the local Ollama instance to test reachability."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> List[str]:
        """Fetch list of local models available in Ollama."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    return [m.get("name", "") for m in data.get("models", [])]
        except Exception as e:
            logger.warning(f"Failed to query Ollama models: {e}")
        return []

    async def get_model_info(self, model: Optional[str] = None) -> Dict[str, Any]:
        """Fetch metadata and architecture parameters for a model from Ollama /api/show."""
        target_model = model or self._model_name
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.post(
                    f"{self.base_url}/api/show",
                    json={"name": target_model}
                )
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.warning(f"Failed to fetch model info for {target_model}: {e}")
        return {}

    async def generate(self, prompt: str, system: Optional[str] = None, format_json: bool = False) -> str:
        """
        Request text completion from the local open-weight model via Ollama.
        Supports both Gemma and Qwen3 architectures.
        """
        payload = {
            "model": self._model_name,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": 260,
            }
        }
        if format_json:
            payload["format"] = "json"
        if system:
            payload["system"] = system

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "").strip()
                else:
                    raise RuntimeError(f"Ollama returned status code {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"Ollama generation error ({self._model_name}): {e}")
            raise e
