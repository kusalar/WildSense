import base64
import logging
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx

from config import (
    AUDIO_PROVIDER,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    ELEVENLABS_MODEL_ID,
    ELEVENLABS_TIMEOUT_SECONDS,
)

logger = logging.getLogger("wildsense.audio")


def format_mission_narration(mission: Dict[str, Any]) -> str:
    """
    Format a validated mission into a concise, calm spoken instruction
    suitable for outdoor nature exploration (target duration ~15-35 seconds).
    Avoids reading JSON keys, markdown artifacts, or technical jargon.
    """
    title = str(mission.get("title", "")).strip()
    instruction = str(mission.get("instruction", "")).strip()
    physical_action = str(mission.get("physical_action", "")).strip()
    observation_goal = str(mission.get("observation_goal", "")).strip()
    safety_note = str(mission.get("safety_note", "")).strip()
    estimated_minutes = mission.get("estimated_minutes")

    def clean_text(val: str) -> str:
        # Strip markdown bold/italics/backticks/brackets
        cleaned = re.sub(r"[*_#`\[\]]", "", val)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if cleaned and cleaned[-1] not in ".!?":
            cleaned += "."
        return cleaned

    parts = []
    if title:
        parts.append(clean_text(title))

    if estimated_minutes:
        try:
            m = int(estimated_minutes)
            if m > 0:
                parts.append(f"Plan for a {m}-minute observation.")
        except (ValueError, TypeError):
            pass

    if instruction:
        parts.append(clean_text(instruction))

    if physical_action:
        cleaned_act = clean_text(physical_action)
        # Avoid redundancy if action is already largely mentioned in instruction
        if cleaned_act.lower() not in instruction.lower():
            parts.append(cleaned_act)

    if observation_goal:
        cleaned_goal = clean_text(observation_goal)
        if cleaned_goal.lower() not in instruction.lower():
            parts.append(f"Observation goal: {cleaned_goal}")

    if safety_note:
        parts.append(f"Safety note: {clean_text(safety_note)}")

    narration = " ".join(parts).strip()
    return narration if narration else "Observe your surroundings closely and calmly."


class AudioMissionProvider(ABC):
    """
    Abstract interface for audio mission narration.
    Allows seamlessly plugging in ElevenLabs or local browser TTS
    without changing client contracts.
    """
    provider_name: str = "base"

    @abstractmethod
    async def generate_audio(self, text: str) -> Dict[str, Any]:
        """Generate audio synthesis metadata or in-memory playback payload."""
        pass

    async def synthesize_bytes(self, text: str) -> bytes:
        """Synthesize raw audio bytes (MP3/WAV) in memory if supported."""
        raise NotImplementedError("This provider does not support binary synthesis.")


class MockAudioProvider(AudioMissionProvider):
    """
    Default offline audio provider that emits structured narration cues
    used by the frontend's Web Speech API.
    """

    def __init__(self, provider_name: str = "mock-audio-synthesizer"):
        self.provider_name = provider_name

    async def generate_audio(self, text: str) -> Dict[str, Any]:
        cleaned_text = text.strip()
        word_count = len(cleaned_text.split())
        estimated_duration = max(2.0, round(word_count / 2.5, 1))

        return {
            "status": "ready",
            "provider": self.provider_name,
            "text": cleaned_text,
            "duration_seconds": estimated_duration,
            "supports_client_speech": True,
            "audio_url": None,
            "audio_base64": None,
            "speech_rate": 0.92,
            "pitch": 0.95
        }


class BrowserAudioProvider(MockAudioProvider):
    """Browser-based speech synthesis provider."""

    def __init__(self):
        super().__init__(provider_name="browser")


class ElevenLabsAudioProvider(AudioMissionProvider):
    """
    Genuine ElevenLabs Text-to-Speech API integration.
    Performs streaming or in-memory synthesis via official REST endpoint:
    POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        self.provider_name = "elevenlabs"
        self.api_key = (api_key if api_key is not None else ELEVENLABS_API_KEY).strip()
        self.voice_id = (voice_id if voice_id is not None else ELEVENLABS_VOICE_ID).strip()
        self.model_id = (model_id if model_id is not None else (ELEVENLABS_MODEL_ID or "eleven_flash_v2_5")).strip()
        self.timeout_seconds = timeout_seconds or ELEVENLABS_TIMEOUT_SECONDS
        self._http_client = http_client


    def is_configured(self) -> bool:
        """Return True if both API key and Voice ID are configured."""
        return bool(self.api_key and self.voice_id)

    async def synthesize_bytes(self, text: str) -> bytes:
        """
        Call ElevenLabs TTS endpoint and return raw MP3 bytes in memory.
        Does not write to disk. Never logs sensitive keys.
        """
        if not self.api_key:
            raise ValueError("ElevenLabs API key is not configured.")
        if not self.voice_id:
            raise ValueError("ElevenLabs voice ID is not configured.")

        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Narration text is empty.")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        payload = {
            "text": cleaned_text,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.50,
                "similarity_boost": 0.75
            }
        }

        # Safe logging without exposing secret key
        masked_key = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "***"
        logger.info(
            "Calling ElevenLabs TTS (voice_id=%s, model=%s, key=%s, text_len=%d)",
            self.voice_id,
            self.model_id,
            masked_key,
            len(cleaned_text)
        )

        try:
            if self._http_client:
                response = await self._http_client.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout_seconds
                )
            else:
                async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                    response = await client.post(
                        url,
                        headers=headers,
                        json=payload
                    )

            if response.status_code == 401 or response.status_code == 403:
                raise PermissionError("ElevenLabs authentication failed. Verify ELEVENLABS_API_KEY.")
            elif response.status_code == 429:
                raise RuntimeError("ElevenLabs rate limit or quota exceeded.")
            elif response.status_code == 404:
                raise ValueError(f"Configured ElevenLabs voice ID '{self.voice_id}' was not found.")
            elif response.status_code >= 400:
                raise RuntimeError(f"ElevenLabs API returned HTTP {response.status_code}: {response.text[:150]}")

            audio_bytes = response.content
            if not audio_bytes:
                raise RuntimeError("ElevenLabs returned empty audio payload.")

            return audio_bytes

        except httpx.TimeoutException:
            logger.warning("ElevenLabs TTS request timed out after %.1fs", self.timeout_seconds)
            raise TimeoutError(f"ElevenLabs TTS timed out after {self.timeout_seconds}s")
        except httpx.RequestError as exc:
            logger.warning("Network error reaching ElevenLabs: %s", type(exc).__name__)
            raise ConnectionError(f"Could not reach ElevenLabs audio service: {type(exc).__name__}")

    async def generate_audio(self, text: str) -> Dict[str, Any]:
        """
        Synthesize audio and return an in-memory base64 data URI response.
        Leaves persistent disk untouched.
        """
        cleaned_text = text.strip()
        audio_bytes = await self.synthesize_bytes(cleaned_text)

        b64_audio = base64.b64encode(audio_bytes).decode("ascii")
        data_url = f"data:audio/mpeg;base64,{b64_audio}"

        # Estimate duration based on word count (~2.5 words/sec) or byte heuristic
        words = len(cleaned_text.split())
        estimated_duration = max(2.0, round(words / 2.6, 1))

        return {
            "status": "ready",
            "provider": "elevenlabs",
            "text": cleaned_text,
            "duration_seconds": estimated_duration,
            "supports_client_speech": False,
            "audio_url": data_url,
            "audio_base64": b64_audio,
            "model": self.model_id,
            "voice_id": self.voice_id,
            "speech_rate": 1.0,
            "pitch": 1.0
        }


def get_audio_provider(provider_type: Optional[str] = None) -> AudioMissionProvider:
    """
    Factory for audio providers.
    Uses AUDIO_PROVIDER config by default unless explicitly overridden.
    """
    ptype = (provider_type or AUDIO_PROVIDER or "browser").lower().strip()
    if ptype == "elevenlabs":
        return ElevenLabsAudioProvider()
    elif ptype == "mock" or ptype == "mock-audio-synthesizer":
        return MockAudioProvider()
    return BrowserAudioProvider()


async def generate_audio_with_fallback(
    text: str,
    preferred_provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Orchestrates safe audio generation:
    1. If user or system requests 'browser', uses BrowserAudioProvider (never touches cloud).
    2. If 'elevenlabs' is requested, attempts ElevenLabsAudioProvider.
    3. If ElevenLabs is unconfigured, times out, rate limits, or errors, safely falls back
       to BrowserAudioProvider with an accurate explanation and without failing the mission.
    """
    target = (preferred_provider or AUDIO_PROVIDER or "browser").lower().strip()

    if target != "elevenlabs":
        # Pure offline local browser speech
        browser_provider = BrowserAudioProvider()
        return await browser_provider.generate_audio(text)

    # ElevenLabs requested
    eleven_provider = ElevenLabsAudioProvider()
    if not eleven_provider.is_configured():
        logger.info("ElevenLabs credentials not configured. Falling back to browser speech.")
        browser_provider = BrowserAudioProvider()
        fallback_res = await browser_provider.generate_audio(text)
        fallback_res["status"] = "fallback"
        fallback_res["fallback_reason"] = "ElevenLabs not configured (missing ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID)"
        return fallback_res

    try:
        return await eleven_provider.generate_audio(text)
    except Exception as exc:
        logger.warning("ElevenLabs generation failed (%s). Falling back to browser speech.", str(exc))
        browser_provider = BrowserAudioProvider()
        fallback_res = await browser_provider.generate_audio(text)
        fallback_res["status"] = "fallback"
        fallback_res["fallback_reason"] = f"ElevenLabs unavailable: {str(exc)}"
        return fallback_res
