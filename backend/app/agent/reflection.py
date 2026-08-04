from __future__ import annotations

from typing import Dict


class ReflectionEngine:
    def summarize(self, goal: str, outcome: str, details: Dict[str, object]) -> Dict[str, object]:
        return {
            "goal": goal,
            "outcome": outcome,
            "details": details,
            "summary": f"Goal '{goal}' completed with status '{outcome}'.",
        }
