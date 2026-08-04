from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class StartVoiceResponse(BaseModel):
    listening: bool
    speaking: bool
    wake_word_active: bool


class StopVoiceResponse(BaseModel):
    listening: bool
    speaking: bool
    wake_word_active: bool


class VoiceTranscribeRequest(BaseModel):
    text: Optional[str] = Field(default=None)
    execute_command: bool = Field(default=False)
    conversation_id: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)


class VoiceTranscribeResponse(BaseModel):
    transcript: str
    wake_word_active: bool
    command_text: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None


class VoiceSpeakRequest(BaseModel):
    text: str
    voice: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    speed: Optional[float] = Field(default=None)


class VoiceSettingsResponse(BaseModel):
    wake_word: str
    language: str
    voice_name: str
    speed: float
    stt_engine: str
    tts_engine: str
    streaming: bool


class VoiceSettingsUpdateRequest(BaseModel):
    wake_word: Optional[str] = None
    language: Optional[str] = None
    voice_name: Optional[str] = None
    speed: Optional[float] = None
    stt_engine: Optional[str] = None
    tts_engine: Optional[str] = None
    streaming: Optional[bool] = None
