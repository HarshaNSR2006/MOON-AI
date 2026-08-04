from __future__ import annotations

from typing import Optional


class VoiceRecorder:
    def __init__(self) -> None:
        self._recording = False
        self._audio_data: bytes = b""

    def start(self) -> None:
        self._recording = True
        self._audio_data = b""

    def stop(self) -> bytes:
        self._recording = False
        return self._audio_data

    def append(self, audio_bytes: bytes) -> None:
        if self._recording:
            self._audio_data += audio_bytes

    def get_audio(self) -> bytes:
        return self._audio_data

    def is_recording(self) -> bool:
        return self._recording
