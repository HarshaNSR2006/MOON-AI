from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class PluginState(str, Enum):
    DISCOVERED = "discovered"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    ENABLED = "enabled"
    DISABLED = "disabled"
    FAILED = "failed"
    UNLOADED = "unloaded"


@dataclass
class PluginRecord:
    name: str
    path: str
    state: PluginState = PluginState.DISCOVERED
    manifest: Optional[dict[str, Any]] = None
    instance: Optional[Any] = None
    error: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
