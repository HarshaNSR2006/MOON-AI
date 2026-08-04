from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.logger import logger
from app.commands.manager import command_manager
from app.schemas.command import CommandPlan, CommandStep
from app.schemas.automation import (
    RunRequest,
    TaskRecord,
    TaskStatus,
    RunResponse,
    TaskSummary,
)


HISTORY_PATH = Path(__file__).resolve().parents[2] / "logs" / "automation_history.json"
HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class InternalTask:
    id: str
    workflow: Dict[str, Any]
    status: TaskStatus = TaskStatus.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


class AutomationEngine:
    def __init__(self) -> None:
        self.tasks: Dict[str, InternalTask] = {}
        self._lock = asyncio.Lock()

    async def run_workflow(self, payload: RunRequest) -> RunResponse:
        task_id = str(uuid.uuid4())
        task = InternalTask(id=task_id, workflow=payload.workflow)
        self.tasks[task_id] = task

        # Run in background
        asyncio.create_task(self._execute_task(task, payload.allow_dangerous))

        logger.info("Queued workflow %s", task_id)
        return RunResponse(task_id=task_id, status=task.status.value)

    async def _execute_task(self, task: InternalTask, allow_dangerous: bool) -> None:
        async with self._lock:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now(timezone.utc)
            self._persist()

        try:
            # Convert incoming workflow steps into CommandPlan
            steps = [CommandStep(command=s.get("command"), args=s.get("args", {})) for s in task.workflow.get("steps", [])]
            plan = CommandPlan(steps=steps)

            # Use existing command manager to execute plan
            result = command_manager.executor.execute_plan(plan, allow_dangerous=allow_dangerous)

            task.result = {"success": result.success, "results": [r.model_dump() for r in result.results]}
            task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED

        except Exception as exc:  # noqa: BLE001 - capture to mark failure
            logger.exception("Workflow %s failed: %s", task.id, exc)
            task.result = {"error": str(exc)}
            task.status = TaskStatus.FAILED

        task.finished_at = datetime.now(timezone.utc)
        self._persist()

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        task = self.tasks.get(task_id)
        if task is None:
            return None
        return TaskRecord(
            id=task.id,
            status=task.status,
            created_at=task.created_at,
            started_at=task.started_at,
            finished_at=task.finished_at,
            result=task.result or {},
        )

    def list_tasks(self) -> List[TaskSummary]:
        return [TaskSummary(id=t.id, status=t.status) for t in self.tasks.values()]

    def _persist(self) -> None:
        try:
            serial = [
                {
                    "id": t.id,
                    "workflow": t.workflow,
                    "status": t.status.value,
                    "created_at": t.created_at.isoformat(),
                    "started_at": t.started_at.isoformat() if t.started_at else None,
                    "finished_at": t.finished_at.isoformat() if t.finished_at else None,
                    "result": t.result,
                }
                for t in self.tasks.values()
            ]
            with HISTORY_PATH.open("w", encoding="utf-8") as handle:
                json.dump(serial, handle, indent=2)
        except Exception:
            logger.exception("Failed to persist automation history")


engine = AutomationEngine()
