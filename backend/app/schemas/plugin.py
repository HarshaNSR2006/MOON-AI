from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PluginManifest(BaseModel):
    name: str
    version: str
    author: str
    description: str
    permissions: List[str] = Field(default_factory=list)


class PluginInfo(BaseModel):
    name: str
    path: str
    state: str
    manifest: Optional[PluginManifest] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
