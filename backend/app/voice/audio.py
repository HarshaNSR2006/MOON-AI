from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AudioBuffer:
    data: bytes
    sample_rate: int = 16000
    channels: int = 1
