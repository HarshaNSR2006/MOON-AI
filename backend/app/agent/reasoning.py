from __future__ import annotations

from typing import Any, Dict, Optional


class ReasoningEngine:
    def summarize(self, goal: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        analysis = (metadata or {}).get("goal_analysis", {}) if metadata else {}
        tools = (metadata or {}).get("tool_suggestion", {}).get("selected", []) if metadata else []
        return {
            "goal": goal,
            "category": analysis.get("category", "general"),
            "capabilities": analysis.get("capabilities", "general"),
            "tools": tools,
            "strategy": "break_goal_into_tasks_and_execute_sequentially",
        }
