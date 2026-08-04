from __future__ import annotations

import re
from typing import Any, Dict, Optional

from app.commands.manager import command_manager
from app.core.logger import logger
from app.voice.language import is_supported
from app.voice.recorder import VoiceRecorder
from app.voice.settings import voice_settings
from app.voice.stt import SpeechToTextEngine
from app.voice.tts import TextToSpeechEngine
from app.voice.vad import VoiceActivityDetector
from app.voice.wakeword import WakeWordDetector


class VoiceManager:
    def __init__(self) -> None:
        self.settings = voice_settings
        self.state: Dict[str, Any] = {
            "listening": False,
            "speaking": False,
            "wake_word_active": False,
        }
        self.recorder = VoiceRecorder()
        self.stt_engine = SpeechToTextEngine()
        self.tts_engine = TextToSpeechEngine()
        self.vad = VoiceActivityDetector()
        self.wakeword = WakeWordDetector(self.settings.wake_word)

    def start(self) -> Dict[str, Any]:
        self.state["listening"] = True
        self.recorder.start()
        logger.info("Voice engine started")
        return self.state.copy()

    def stop(self) -> Dict[str, Any]:
        self.state["listening"] = False
        self.state["speaking"] = False
        self.state["wake_word_active"] = False
        if self.recorder.is_recording():
            self.recorder.stop()
        logger.info("Voice engine stopped")
        return self.state.copy()

    def transcribe(
        self,
        text: Optional[str] = None,
        audio_data: Optional[bytes] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        if text is not None:
            logger.info("Using provided transcript text")
            transcript = text.strip()
        elif audio_data is not None:
            transcript = self.stt_engine.transcribe(audio_data, language)
        else:
            raise ValueError("Either text or audio_data must be provided for transcription.")

        self.state["wake_word_active"] = self.wakeword.detect_text(transcript)
        return {"transcript": transcript, "wake_word_active": self.state["wake_word_active"]}

    def speak(
        self,
        text: str,
        voice: Optional[str] = None,
        language: Optional[str] = None,
        speed: Optional[float] = None,
    ) -> Dict[str, Any]:
        self.state["speaking"] = True
        result = self.tts_engine.speak(text, voice=voice, language=language, speed=speed)
        self.state["speaking"] = False
        return result

    def get_settings(self) -> Dict[str, Any]:
        return {
            "wake_word": self.settings.wake_word,
            "language": self.settings.language,
            "voice_name": self.settings.voice_name,
            "speed": self.settings.speed,
            "stt_engine": self.settings.stt_engine,
            "tts_engine": self.settings.tts_engine,
            "streaming": self.settings.streaming,
        }

    def update_settings(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        if "wake_word" in updates:
            self.settings.wake_word = updates["wake_word"]
            self.wakeword = WakeWordDetector(self.settings.wake_word)
        if "language" in updates:
            if not is_supported(updates["language"]):
                raise ValueError(f"Unsupported language '{updates['language']}'")
            self.settings.language = updates["language"]
        if "voice_name" in updates:
            self.settings.voice_name = updates["voice_name"]
        if "speed" in updates:
            self.settings.speed = float(updates["speed"])
        if "stt_engine" in updates:
            self.settings.stt_engine = updates["stt_engine"]
        if "tts_engine" in updates:
            self.settings.tts_engine = updates["tts_engine"]
        if "streaming" in updates:
            self.settings.streaming = bool(updates["streaming"])
        return self.get_settings()

    def handle_transcript(
        self,
        transcript: str,
        conversation_id: Optional[str] = None,
        execute_command: bool = False,
    ) -> Dict[str, Any]:
        if not transcript:
            return {"transcript": "", "result": None}

        command_text = transcript
        if self.wakeword.detect_text(transcript):
            command_text = transcript.lower().replace(self.settings.wake_word.lower(), "", 1).strip()
            command_text = re.sub(r"^(hey|ok|hi|hello)\s+", "", command_text).strip()

        response: Dict[str, Any] = {
            "transcript": transcript,
            "command_text": command_text,
            "plan": None,
            "result": None,
        }
        if execute_command and command_text:
            from app.schemas.command import CommandExecutionRequest, CommandPlanRequest

            plan = command_manager.plan(
                CommandPlanRequest(query=command_text, conversation_id=conversation_id)
            )
            request = CommandExecutionRequest(plan=plan, allow_dangerous=False)
            result = command_manager.execute(request)
            response["plan"] = plan.model_dump()
            response["result"] = result.model_dump()
        return response


voice_manager = VoiceManager()
