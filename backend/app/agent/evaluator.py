from __future__ import annotations

from typing import Dict

from app.agent.state import AgentTaskStatus


class ResultEvaluator:
    def evaluate_task(self, task_result: Dict[str, object]) -> bool:
        if task_result.get("status") == "failed":
            return False
        return True

    def should_retry(self, task_status: AgentTaskStatus, attempt: int, max_retries: int = 1) -> bool:
        if task_status != AgentTaskStatus.FAILED:
            return False
        return attempt < max_retries
