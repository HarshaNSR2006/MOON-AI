from __future__ import annotations

from typing import Optional

from app.core.logger import logger
from app.voice.language import is_supported
from app.voice.settings import voice_settings
from app.voice.voices import get_voice


class TextToSpeechEngine:
    def speak(
        self,
        text: str,
        voice: Optional[str] = None,
        language: Optional[str] = None,
        speed: Optional[float] = None,
    ) -> dict[str, str]:
        language = language or voice_settings.language
        voice_name = voice or voice_settings.voice_name
        speed = speed or voice_settings.speed
        if not is_supported(language):
            raise ValueError(f"Unsupported language '{language}' for TTS.")
        if get_voice(voice_name) is None:
            raise ValueError(f"Voice '{voice_name}' is not available.")
        logger.info(
            "Generating speech using %s engine (voice=%s, language=%s, speed=%s)",
            voice_settings.tts_engine,
            voice_name,
            language,
            speed,
        )
        return {"text": text, "voice": voice_name, "language": language, "speed": speed}
