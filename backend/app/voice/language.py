from __future__ import annotations

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
    "zh": "Chinese",
}


def is_supported(language_code: str) -> bool:
    return language_code in SUPPORTED_LANGUAGES
