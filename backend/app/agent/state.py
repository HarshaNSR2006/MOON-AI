from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentTaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELED = "canceled"


class AgentRunStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


@dataclass
class AgentTask:
    id: str
    name: str
    command: str
    args: Dict[str, Any]
    status: AgentTaskStatus = AgentTaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class AgentRunRecord:
    id: str
    goal: str
    status: AgentRunStatus = AgentRunStatus.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    current_task: Optional[str] = None
    tasks: List[AgentTask] = field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def new_agent_task(name: str, command: str, args: Dict[str, Any], dependencies: Optional[List[str]] = None) -> AgentTask:
    return AgentTask(
        id=str(uuid.uuid4()),
        name=name,
        command=command,
        args=args,
        dependencies=dependencies or [],
    )
