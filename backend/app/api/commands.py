from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.commands.exceptions import (
    CommandNotFound,
    ExecutionFailed,
    InvalidArguments,
    PermissionDenied,
)
from app.commands.manager import command_manager
from app.schemas.command import (
    BatchCommandResult,
    CommandExecutionRequest,
    CommandInfo,
    CommandPlan,
    CommandPlanRequest,
)

router = APIRouter()


@router.post("/plan", response_model=CommandPlan)
async def plan_commands(
    payload: CommandPlanRequest,
    current_user=Depends(get_current_user),
) -> CommandPlan:
    try:
        return command_manager.plan(payload)
    except InvalidArguments as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/execute", response_model=BatchCommandResult)
async def execute_commands(
    payload: CommandExecutionRequest,
    current_user=Depends(get_current_user),
) -> BatchCommandResult:
    try:
        return command_manager.execute(payload)
    except CommandNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))
    except InvalidArguments as error:
        raise HTTPException(status_code=400, detail=str(error))
    except PermissionDenied as error:
        raise HTTPException(status_code=403, detail=str(error))
    except ExecutionFailed as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("", response_model=list[CommandInfo])
def list_commands(current_user=Depends(get_current_user)) -> list[CommandInfo]:
    return command_manager.list_commands()


@router.get("/{command_name}", response_model=CommandInfo)
def get_command(command_name: str, current_user=Depends(get_current_user)) -> CommandInfo:
    try:
        return command_manager.get_command(command_name)
    except CommandNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))
