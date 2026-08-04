from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentTaskModel(BaseModel):
    id: str
    name: str
    command: str
    args: Dict[str, Any]
    status: str
    dependencies: List[str] = Field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AgentRunRequest(BaseModel):
    goal: str
    conversation_id: Optional[str] = None
    allow_dangerous: bool = Field(default=False)


class AgentActionRequest(BaseModel):
    run_id: str


class AgentRunResponse(BaseModel):
    run_id: str
    status: str
    goal: str


class AgentStatusResponse(BaseModel):
    run_id: str
    goal: str
    status: str
    current_task: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


class AgentTaskListResponse(BaseModel):
    tasks: List[AgentTaskModel]


class AgentHistoryEntry(BaseModel):
    id: str
    goal: str
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    current_task: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentRunDetailResponse(BaseModel):
    run_id: str
    goal: str
    status: str
    current_task: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    tasks: List[AgentTaskModel] = Field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
