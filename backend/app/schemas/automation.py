from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class RunRequest(BaseModel):
    workflow: Dict[str, Any] = Field(...)
    allow_dangerous: bool = Field(default=False)


class RunResponse(BaseModel):
    task_id: str
    status: str


class TaskRecord(BaseModel):
    id: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Dict[str, Any] = Field(default_factory=dict)


class TaskSummary(BaseModel):
    id: str
    status: TaskStatus


class TaskListResponse(BaseModel):
    tasks: List[TaskSummary]
