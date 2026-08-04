from typing import Optional

from typing import Optional

from app.commands.exceptions import ExecutionFailed
from app.commands.permissions import check_permission
from app.commands.registry import CommandRegistry, command_registry
from app.commands.result import CommandResult
from app.schemas.command import BatchCommandResult, CommandPlan


class CommandExecutor:
    def __init__(
        self,
        registry: Optional[CommandRegistry] = None,
    ) -> None:
        self.registry = registry or command_registry

    def execute_plan(
        self,
        plan: CommandPlan,
        allow_dangerous: bool = False,
    ) -> BatchCommandResult:
        results: list[CommandResult] = []

        for step in plan.steps:
            command = self.registry.get(step.command)
            check_permission(step.command, allow_dangerous=allow_dangerous)
            try:
                result = command.execute(step.args)
                if not isinstance(result, CommandResult):
                    raise ExecutionFailed(
                        f"Command '{step.command}' did not return a valid result."
                    )
            except Exception as exc:
                result = CommandResult(
                    success=False,
                    command=step.command,
                    message=str(exc),
                    error=type(exc).__name__,
                )
            results.append(result)
            if not result.success:
                break

        return BatchCommandResult(success=all(item.success for item in results), results=results)
