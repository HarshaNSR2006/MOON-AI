from fastapi import APIRouter, Depends, HTTPException

from app.agent.manager import agent_manager
from app.auth.dependencies import get_current_user
from app.schemas.agent import (
    AgentActionRequest,
    AgentRunRequest,
    AgentRunResponse,
    AgentStatusResponse,
    AgentRunDetailResponse,
    AgentHistoryEntry,
)

router = APIRouter()


def _record_to_run_response(record) -> AgentRunResponse:
    return AgentRunResponse(run_id=record.id, status=record.status.value, goal=record.goal)


def _record_to_status_response(record) -> AgentStatusResponse:
    return AgentStatusResponse(
        run_id=record.id,
        goal=record.goal,
        status=record.status.value,
        current_task=record.current_task,
        started_at=record.started_at,
        finished_at=record.finished_at,
        result=record.result,
    )


def _record_to_detail_response(record) -> AgentRunDetailResponse:
    tasks = [
        {
            "id": task.id,
            "name": task.name,
            "command": task.command,
            "args": task.args,
            "status": task.status.value,
            "dependencies": task.dependencies,
            "result": task.result,
            "error": task.error,
        }
        for task in record.tasks
    ]
    return AgentRunDetailResponse(
        run_id=record.id,
        goal=record.goal,
        status=record.status.value,
        current_task=record.current_task,
        started_at=record.started_at,
        finished_at=record.finished_at,
        tasks=tasks,
        result=record.result,
        metadata=record.metadata,
    )


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(payload: AgentRunRequest, current_user=Depends(get_current_user)) -> AgentRunResponse:
    record = await agent_manager.run_goal(
        goal=payload.goal,
        conversation_id=payload.conversation_id,
        allow_dangerous=payload.allow_dangerous,
    )
    return _record_to_run_response(record)


@router.post("/pause", response_model=AgentStatusResponse)
def pause_agent(payload: AgentActionRequest, current_user=Depends(get_current_user)) -> AgentStatusResponse:
    try:
        record = agent_manager.pause_run(payload.run_id)
        return _record_to_status_response(record)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/resume", response_model=AgentStatusResponse)
def resume_agent(payload: AgentActionRequest, current_user=Depends(get_current_user)) -> AgentStatusResponse:
    try:
        record = agent_manager.resume_run(payload.run_id)
        return _record_to_status_response(record)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/cancel", response_model=AgentStatusResponse)
def cancel_agent(payload: AgentActionRequest, current_user=Depends(get_current_user)) -> AgentStatusResponse:
    try:
        record = agent_manager.cancel_run(payload.run_id)
        return _record_to_status_response(record)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/pause/{run_id}", response_model=AgentStatusResponse)
def pause_agent_legacy(run_id: str, current_user=Depends(get_current_user)) -> AgentStatusResponse:
    return pause_agent(AgentActionRequest(run_id=run_id), current_user=current_user)


@router.post("/resume/{run_id}", response_model=AgentStatusResponse)
def resume_agent_legacy(run_id: str, current_user=Depends(get_current_user)) -> AgentStatusResponse:
    return resume_agent(AgentActionRequest(run_id=run_id), current_user=current_user)


@router.post("/cancel/{run_id}", response_model=AgentStatusResponse)
def cancel_agent_legacy(run_id: str, current_user=Depends(get_current_user)) -> AgentStatusResponse:
    return cancel_agent(AgentActionRequest(run_id=run_id), current_user=current_user)


@router.get("/status", response_model=AgentRunDetailResponse)
def get_agent_status_query(run_id: str, current_user=Depends(get_current_user)) -> AgentRunDetailResponse:
    record = agent_manager.get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return _record_to_detail_response(record)


@router.get("/status/{run_id}", response_model=AgentRunDetailResponse)
def get_agent_status(run_id: str, current_user=Depends(get_current_user)) -> AgentRunDetailResponse:
    record = agent_manager.get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return _record_to_detail_response(record)


@router.get("/tasks", response_model=list[AgentRunResponse])
def list_agent_tasks(current_user=Depends(get_current_user)) -> list[AgentRunResponse]:
    return [_record_to_run_response(record) for record in agent_manager.list_runs()]


@router.get("/history", response_model=list[AgentHistoryEntry])
def get_agent_history(current_user=Depends(get_current_user)) -> list[AgentHistoryEntry]:
    history = agent_manager.get_history()
    return [AgentHistoryEntry(**entry) for entry in history]
