from __future__ import annotations

from typing import Any


class WakeWordDetector:
    def __init__(self, wake_word: str = "moon") -> None:
        self.wake_word = wake_word.lower().strip()

    def detect(self, audio_data: bytes) -> bool:
        return False

    def detect_text(self, transcript: str) -> bool:
        return self.wake_word in transcript.lower()
