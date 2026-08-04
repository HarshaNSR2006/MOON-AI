from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.memory.manager import memory_manager
from app.plugins.manager import plugin_manager
from app.ai.context import ContextManager


class ContextBuilder:
    def __init__(self) -> None:
        self.memory_manager = memory_manager
        self.plugin_manager = plugin_manager
        self.conversation_context = ContextManager()

    def build_context(self, goal: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        context: Dict[str, Any] = {
            "goal": goal,
            "conversation_id": conversation_id,
            "available_plugins": [plugin.name for plugin in self.plugin_manager.list_plugins()],
            "recent_memory": [],
            "conversation_history": [],
        }

        if conversation_id:
            try:
                context["conversation_history"] = self.conversation_context.get_conversation(conversation_id).messages
            except Exception:
                context["conversation_history"] = []

            try:
                context["recent_memory"] = [item.content for item in self.memory_manager.list_memories(conversation_id=conversation_id)]
            except Exception:
                context["recent_memory"] = []

        return context
