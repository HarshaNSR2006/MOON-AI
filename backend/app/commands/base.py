from abc import ABC, abstractmethod
from typing import Any, Dict

from app.commands.result import CommandResult


class Command(ABC):
    name: str
    description: str
    args_schema: Dict[str, str] = {}

    @abstractmethod
    def validate(self, args: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> CommandResult:
        raise NotImplementedError

    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "args": self.args_schema,
        }
