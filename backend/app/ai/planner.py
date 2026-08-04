from typing import Any, Optional

from app.commands.manager import command_manager
from app.schemas.command import CommandPlanRequest


class Planner:
    """Simple planner that converts user requests into structured command plans."""

    def __init__(self, config: Any = None) -> None:
        self.config = config

    def plan(self, message: str, conversation_id: Optional[str] = None) -> Any:
        request = CommandPlanRequest(query=message, conversation_id=conversation_id)
        return command_manager.plan(request)
