from __future__ import annotations

from typing import Any, Dict, Optional

from app.agent.goals import GoalAnalyzer
from app.agent.selector import ToolSelector
from app.agent.task_graph import TaskGraph
from app.agent.state import AgentTask, new_agent_task
from app.commands.manager import command_manager
from app.schemas.command import CommandPlanRequest


class AgentPlanner:
    def __init__(self) -> None:
        self.analyzer = GoalAnalyzer()
        self.selector = ToolSelector()

    def prepare_task_graph(self, goal: str, context: Optional[Dict[str, Any]] = None) -> TaskGraph:
        analysis = self.analyzer.analyze(goal)
        tools = self.selector.select_tools(goal)
        plan = command_manager.plan(CommandPlanRequest(query=goal))

        graph = TaskGraph()
        previous_task_id: str | None = None
        for step in plan.steps:
            task = new_agent_task(
                name=f"Execute {step.command}",
                command=step.command,
                args=step.args,
                dependencies=[previous_task_id] if previous_task_id else [],
            )
            graph.add_task(task)
            previous_task_id = task.id

        if not graph.nodes:
            task = new_agent_task(
                name=f"Interpret goal: {goal}",
                command="search_web",
                args={"query": goal},
            )
            graph.add_task(task)

        graph.metadata = {
            "goal_analysis": analysis,
            "tool_suggestion": tools,
        }
        return graph
