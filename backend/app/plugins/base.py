from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.commands.base import Command
from app.commands.result import CommandResult


class BasePlugin(ABC):
    name: str = ""
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = ""
    permissions: List[str] = []
    manifest: Dict[str, Any] = {}

    def __init__(self) -> None:
        self.commands: List[Command] = []
        self.events: List[str] = []
        self.config: Dict[str, Any] = {}

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        return None

    def register_command(self, command: Command) -> None:
        self.commands.append(command)

    def register_event(self, event_name: str) -> None:
        self.events.append(event_name)

    def get_manifest(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "permissions": list(self.permissions),
        }
