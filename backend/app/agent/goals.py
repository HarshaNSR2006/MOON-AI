from __future__ import annotations

from typing import Dict


class GoalAnalyzer:
    def analyze(self, goal: str) -> Dict[str, str]:
        normalized = goal.strip()
        capabilities = []
        lower = normalized.lower()

        if any(keyword in lower for keyword in ["project", "website", "application", "app"]):
            capabilities.append("filesystem")
        if any(keyword in lower for keyword in ["open", "launch", "run"]):
            capabilities.append("desktop")
        if any(keyword in lower for keyword in ["search", "browse", "google", "documentation"]):
            capabilities.append("browser")
        if any(keyword in lower for keyword in ["memory", "remember", "recall"]):
            capabilities.append("memory")

        return {
            "goal": normalized,
            "category": capabilities[0] if capabilities else "general",
            "capabilities": ",".join(capabilities) if capabilities else "general",
        }
