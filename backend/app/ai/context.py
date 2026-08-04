from typing import Dict

from app.ai.conversation import Conversation
from app.core.config import settings


DEFAULT_SYSTEM_PROMPT = (
    "You are MOON AI, a helpful, friendly assistant. "
    "Answer clearly, keep responses concise, and ask clarifying questions when needed."
)


class ContextManager:
    def __init__(self) -> None:
        self.conversations: Dict[str, Conversation] = {}
        self.max_messages = settings.max_context_messages

    def get_conversation(self, conversation_id: str) -> Conversation:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation(
                conversation_id=conversation_id,
                system_prompt=DEFAULT_SYSTEM_PROMPT,
            )
        conversation = self.conversations[conversation_id]
        conversation.trim_history(self.max_messages)
        return conversation

    def clear_conversation(self, conversation_id: str) -> None:
        self.conversations.pop(conversation_id, None)

    def list_conversations(self) -> Dict[str, Conversation]:
        return dict(self.conversations)
