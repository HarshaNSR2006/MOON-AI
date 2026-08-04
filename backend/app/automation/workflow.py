from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowTemplate:
    name: str
    description: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkflowInstance:
    id: str
    template: WorkflowTemplate
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
    state: str | None = None
    result: Optional[Dict[str, Any]] = None
