from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.core.config import settings


@dataclass
class VoiceSettings:
    wake_word: str = settings.voice_wake_word
    language: str = settings.voice_language
    voice_name: str = settings.voice_name
    speed: float = settings.voice_speed
    stt_engine: str = settings.stt_engine
    tts_engine: str = settings.tts_engine
    streaming: bool = settings.voice_streaming


voice_settings = VoiceSettings()
