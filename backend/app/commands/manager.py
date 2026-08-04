from app.commands.executor import CommandExecutor
from app.commands.parser import CommandParser
from app.commands.planner import CommandPlanner
from app.commands.registry import command_registry
from app.schemas.command import (
    CommandExecutionRequest,
    CommandInfo,
    CommandPlan,
    CommandPlanRequest,
)


class CommandManager:
    def __init__(self) -> None:
        self.registry = command_registry
        self.parser = CommandParser(self.registry)
        self.executor = CommandExecutor(self.registry)
        self.planner = CommandPlanner()

    def list_commands(self) -> list[CommandInfo]:
        return [CommandInfo(**command.info()) for command in self.registry.list()]

    def get_command(self, name: str) -> CommandInfo:
        command = self.registry.get(name)
        return CommandInfo(**command.info())

    def plan(self, request: CommandPlanRequest) -> CommandPlan:
        return self.planner.plan(request)

    def execute(self, request: CommandExecutionRequest) -> "BatchCommandResult":
        plan = self.parser.parse_execution_request(request)
        return self.executor.execute_plan(plan, allow_dangerous=request.allow_dangerous)


command_manager = CommandManager()
