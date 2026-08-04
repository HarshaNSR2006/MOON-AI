import os
from pathlib import Path

import pytest

from app.commands.exceptions import CommandNotFound, PermissionDenied
from app.commands.manager import command_manager
from app.schemas.command import CommandExecutionRequest, CommandPlanRequest


def test_command_registry_includes_core_commands() -> None:
    commands = command_manager.list_commands()
    names = {command.name for command in commands}

    assert "open_app" in names
    assert "search_web" in names
    assert "create_folder" in names
    assert "read_file" in names
    assert "write_file" in names


def test_command_planner_generates_multiple_steps() -> None:
    plan = command_manager.plan(
        CommandPlanRequest(query="Open Chrome and then search FastAPI documentation")
    )

    assert len(plan.steps) == 2
    assert plan.steps[0].command == "open_app"
    assert "chrome" in plan.steps[0].args["name"].lower()
    assert plan.steps[1].command == "search_web"
    assert "FastAPI" in plan.steps[1].args["query"]


def test_command_executor_creates_folder(tmp_path: Path) -> None:
    folder_path = tmp_path / "example-folder"
    request = CommandExecutionRequest(command="create_folder", args={"path": str(folder_path)})

    result = command_manager.execute(request)

    assert result.success
    assert folder_path.exists()
    assert folder_path.is_dir()
    assert result.results[0].command == "create_folder"


def test_command_executor_requires_allow_dangerous_for_delete(tmp_path: Path) -> None:
    file_path = tmp_path / "delete-me.txt"
    file_path.write_text("delete me")
    request = CommandExecutionRequest(command="delete_file", args={"path": str(file_path)})

    with pytest.raises(PermissionDenied):
        command_manager.execute(request)


def test_command_executor_raises_for_unknown_command() -> None:
    request = CommandExecutionRequest(command="unknown_command", args={})

    with pytest.raises(CommandNotFound):
        command_manager.execute(request)
