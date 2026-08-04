from __future__ import annotations

from typing import Optional

from app.core.logger import logger
from app.voice.language import is_supported
from app.voice.settings import voice_settings


class SpeechToTextEngine:
    def transcribe(self, audio_data: bytes, language: Optional[str] = None) -> str:
        language = language or voice_settings.language
        if not is_supported(language):
            raise ValueError(f"Unsupported language '{language}' for STT.")
        logger.info("Transcribing audio using %s engine", voice_settings.stt_engine)
        return "[transcribed speech]"
