from __future__ import annotations


class VoiceActivityDetector:
    def __init__(self) -> None:
        pass

    def is_speech(self, audio_chunk: bytes) -> bool:
        return bool(audio_chunk)
