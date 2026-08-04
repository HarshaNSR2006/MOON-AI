from typing import Optional

from app.commands.exceptions import InvalidArguments
from app.commands.registry import CommandRegistry, command_registry
from app.schemas.command import CommandExecutionRequest, CommandPlan, CommandStep


class CommandParser:
    def __init__(self, registry: Optional[CommandRegistry] = None) -> None:
        self.registry = registry or command_registry

    def validate_plan(self, plan: CommandPlan) -> CommandPlan:
        if not plan.steps:
            raise InvalidArguments("Command plan must include at least one step.")

        for step in plan.steps:
            command = self.registry.get(step.command)
            command.validate(step.args)

        return plan

    def parse_execution_request(self, request: CommandExecutionRequest) -> CommandPlan:
        if request.plan is not None:
            plan = request.plan
        else:
            plan = CommandPlan(steps=[CommandStep(command=request.command, args=request.args)])

        return self.validate_plan(plan)
