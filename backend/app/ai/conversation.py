from typing import List

from app.ai.models import ChatMessage


class Conversation:
    def __init__(self, conversation_id: str, system_prompt: str) -> None:
        self.conversation_id = conversation_id
        self.system_prompt = system_prompt
        self.messages: List[ChatMessage] = []

    def add_user_message(self, content: str) -> None:
        self.messages.append(ChatMessage(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(ChatMessage(role="assistant", content=content))

    def get_history(self) -> List[ChatMessage]:
        return list(self.messages)

    def trim_history(self, max_messages: int) -> None:
        if len(self.messages) <= max_messages:
            return
        self.messages = self.messages[-max_messages:]
