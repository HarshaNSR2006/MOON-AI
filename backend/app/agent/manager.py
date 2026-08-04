from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.agent.context import ContextBuilder
from app.agent.evaluator import ResultEvaluator
from app.agent.executor import AgentExecutor
from app.agent.history import read_history, write_history
from app.agent.planner import AgentPlanner
from app.agent.reasoning import ReasoningEngine
from app.agent.reflection import ReflectionEngine
from app.agent.retry import RetryPolicy
from app.agent.state import AgentRunRecord, AgentRunStatus, AgentTask, AgentTaskStatus
from app.core.logger import logger


class AgentManager:
    def __init__(self) -> None:
        self.planner = AgentPlanner()
        self.executor = AgentExecutor()
        self.evaluator = ResultEvaluator()
        self.reflection = ReflectionEngine()
        self.reasoner = ReasoningEngine()
        self.retry_policy = RetryPolicy()
        self.context_builder = ContextBuilder()
        self.runs: Dict[str, AgentRunRecord] = {}
        self.history = read_history()
        self._lock = asyncio.Lock()

    async def run_goal(
        self,
        goal: str,
        conversation_id: Optional[str] = None,
        allow_dangerous: bool = False,
        background: bool = True,
    ) -> AgentRunRecord:
        run_id = str(uuid.uuid4())
        record = AgentRunRecord(id=run_id, goal=goal)
        self.runs[run_id] = record

        if background:
            asyncio.create_task(self._execute_run(record, conversation_id, allow_dangerous))
        else:
            await self._execute_run(record, conversation_id, allow_dangerous)

        return record

    async def _execute_run(
        self,
        record: AgentRunRecord,
        conversation_id: Optional[str],
        allow_dangerous: bool,
    ) -> None:
        async with self._lock:
            record.status = AgentRunStatus.RUNNING
            record.started_at = datetime.now(timezone.utc)
            context = self.context_builder.build_context(record.goal, conversation_id)
            record.metadata = {
                "goal_analysis": context.get("goal_analysis"),
                "available_plugins": context.get("available_plugins", []),
            }

        task_graph = self.planner.prepare_task_graph(record.goal, context=context)
        record.tasks = list(task_graph.get_ordered_tasks())

        try:
            while record.status == AgentRunStatus.PAUSED:
                await asyncio.sleep(0.25)
            if record.status != AgentRunStatus.CANCELED:
                result_summary = self.executor.execute(record, task_graph, allow_dangerous=allow_dangerous)
                record.result = result_summary
                if result_summary.get("status") == "completed":
                    record.status = AgentRunStatus.COMPLETED
                else:
                    record.status = AgentRunStatus.FAILED
            else:
                logger.info("Agent run %s canceled before execution", record.id)
                record.result = {"status": "canceled"}
        except Exception as exc:
            logger.exception("Agent run %s failed with exception: %s", record.id, exc)
            record.status = AgentRunStatus.FAILED
            record.result = {"status": "failed", "error": str(exc)}
        finally:
            record.finished_at = datetime.now(timezone.utc)
            self._save_history(record)

    def pause_run(self, run_id: str) -> AgentRunRecord:
        run = self.get_run(run_id)
        if run is None:
            raise KeyError(f"Run '{run_id}' not found")
        if run.status == AgentRunStatus.RUNNING:
            run.status = AgentRunStatus.PAUSED
        return run

    def resume_run(self, run_id: str) -> AgentRunRecord:
        run = self.get_run(run_id)
        if run is None:
            raise KeyError(f"Run '{run_id}' not found")
        if run.status == AgentRunStatus.PAUSED:
            run.status = AgentRunStatus.RUNNING
        return run

    def cancel_run(self, run_id: str) -> AgentRunRecord:
        run = self.get_run(run_id)
        if run is None:
            raise KeyError(f"Run '{run_id}' not found")
        run.status = AgentRunStatus.CANCELED
        return run

    def get_run(self, run_id: str) -> Optional[AgentRunRecord]:
        return self.runs.get(run_id)

    def list_runs(self) -> List[AgentRunRecord]:
        return list(self.runs.values())

    def get_history(self) -> List[Dict[str, object]]:
        return self.history

    def _save_history(self, run: AgentRunRecord) -> None:
        entry = {
            "id": run.id,
            "goal": run.goal,
            "status": run.status.value,
            "created_at": run.created_at.isoformat(),
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "finished_at": run.finished_at.isoformat() if run.finished_at else None,
            "current_task": run.current_task,
            "result": run.result,
            "metadata": run.metadata,
        }
        self.history.append(entry)
        write_history(self.history)


agent_manager = AgentManager()
