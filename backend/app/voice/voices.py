from __future__ import annotations

AVAILABLE_VOICES = [
    {"name": "default", "language": "en", "description": "Default assistant voice"},
    {"name": "warm", "language": "en", "description": "Warm, natural voice"},
    {"name": "bright", "language": "en", "description": "Bright and friendly voice"},
]


def get_voice(name: str) -> dict[str, str] | None:
    return next((voice for voice in AVAILABLE_VOICES if voice["name"] == name), None)
