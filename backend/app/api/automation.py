from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.automation.engine import engine
from app.schemas.automation import RunRequest, RunResponse, TaskRecord, TaskListResponse, TaskSummary

router = APIRouter()


@router.post("/run", response_model=RunResponse)
async def run_workflow(payload: RunRequest, current_user=Depends(get_current_user)) -> RunResponse:
    return await engine.run_workflow(payload)


@router.get("/tasks", response_model=list[TaskSummary])
def list_tasks(current_user=Depends(get_current_user)) -> list[TaskSummary]:
    return engine.list_tasks()


@router.get("/tasks/{task_id}", response_model=TaskRecord)
def get_task(task_id: str, current_user=Depends(get_current_user)) -> TaskRecord:
    task = engine.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
