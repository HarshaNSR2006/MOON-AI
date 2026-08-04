from __future__ import annotations

from typing import Dict


class RetryPolicy:
    def __init__(self) -> None:
        self.policy = {
            "network": 2,
            "permission": 0,
            "default": 1,
        }

    def max_retries(self, error_type: str) -> int:
        return self.policy.get(error_type.lower(), self.policy["default"])

    def should_retry(self, error_type: str, attempt: int) -> bool:
        return attempt < self.max_retries(error_type)

    def classify(self, error_message: str) -> str:
        lower = error_message.lower()
        if "network" in lower or "timeout" in lower:
            return "network"
        if "permission" in lower or "restricted" in lower:
            return "permission"
        return "default"
