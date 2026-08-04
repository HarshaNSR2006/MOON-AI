from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from app.agent.state import AgentTask


@dataclass
class TaskGraph:
    nodes: Dict[str, AgentTask] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_task(self, task: AgentTask) -> None:
        self.nodes[task.id] = task

    def add_dependency(self, task_id: str, dependency_id: str) -> None:
        task = self.nodes.get(task_id)
        if task is None:
            return
        if dependency_id not in task.dependencies:
            task.dependencies.append(dependency_id)

    def get_ready_tasks(self) -> List[AgentTask]:
        return [
            task
            for task in self.nodes.values()
            if task.status == task.status.PENDING
            and all(self.nodes[dep].status == task.status.COMPLETED for dep in task.dependencies)
        ]

    def get_ordered_tasks(self) -> List[AgentTask]:
        ordered: List[AgentTask] = []
        visited: set[str] = set()

        def visit(task: AgentTask) -> None:
            if task.id in visited:
                return
            for dependency_id in task.dependencies:
                dependency = self.nodes.get(dependency_id)
                if dependency is not None:
                    visit(dependency)
            visited.add(task.id)
            ordered.append(task)

        for task in self.nodes.values():
            visit(task)

        return ordered
