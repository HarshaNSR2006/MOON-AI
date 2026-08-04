from __future__ import annotations

from typing import Dict, Optional

from app.agent.task_graph import TaskGraph
from app.agent.state import AgentRunRecord, AgentTask, AgentTaskStatus
from app.commands.manager import command_manager
from app.schemas.command import CommandExecutionRequest
from app.core.logger import logger


class AgentExecutor:
    def execute_task(self, run: AgentRunRecord, task: AgentTask, allow_dangerous: bool = False) -> Dict[str, Optional[str]]:
        if run.status == run.status.CANCELED:
            logger.info("Run %s was canceled before task %s", run.id, task.id)
            return {"status": "canceled", "message": None}

        run.current_task = task.id
        task.status = AgentTaskStatus.RUNNING
        logger.info("Executing agent task %s: %s", task.id, task.name)

        execution_request = CommandExecutionRequest(plan=None, command=task.command, args=task.args)
        result = command_manager.execute(execution_request)

        task.result = result.model_dump()
        if result.success:
            task.status = AgentTaskStatus.COMPLETED
            logger.info("Task %s completed successfully", task.id)
            return {"status": "completed", "message": result.model_dump()}

        task.status = AgentTaskStatus.FAILED
        task.error = "; ".join([item.error or item.message for item in result.results])
        logger.warning("Task %s failed: %s", task.id, task.error)
        return {"status": "failed", "message": task.error}

    def execute(self, run: AgentRunRecord, task_graph: TaskGraph, allow_dangerous: bool = False) -> Dict[str, Optional[str]]:
        result_summary: Dict[str, Optional[str]] = {"status": "completed", "message": None}
        ordered_tasks = task_graph.get_ordered_tasks()

        for task in ordered_tasks:
            task_result = self.execute_task(run, task, allow_dangerous=allow_dangerous)
            if task_result["status"] != "completed":
                result_summary["status"] = task_result["status"]
                result_summary["message"] = task_result["message"]
                break

        return result_summary
