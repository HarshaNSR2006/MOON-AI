import asyncio
from pathlib import Path

from app.agent.manager import agent_manager
from app.agent.planner import AgentPlanner
from app.agent.reasoning import ReasoningEngine


def test_agent_planner_generates_task_graph() -> None:
    planner = AgentPlanner()
    graph = planner.prepare_task_graph("Create folder test_agent_phase8", context={})
    tasks = graph.get_ordered_tasks()

    assert len(tasks) >= 1
    assert tasks[0].command == "create_folder"
    assert "test_agent_phase8" in tasks[0].args["path"]


def test_agent_manager_runs_goal_and_creates_folder() -> None:
    folder_path = Path("test_agent_phase8_folder")
    if folder_path.exists():
        if folder_path.is_dir():
            for child in folder_path.iterdir():
                if child.is_file():
                    child.unlink()
                else:
                    pass
            folder_path.rmdir()

    async def run_and_wait() -> None:
        record = await agent_manager.run_goal(
            goal=f"Create folder {folder_path}",
            background=False,
            allow_dangerous=False,
        )
        assert record.status.value == "completed"
        assert folder_path.exists() and folder_path.is_dir()

    asyncio.run(run_and_wait())

    if folder_path.exists() and folder_path.is_dir():
        folder_path.rmdir()
