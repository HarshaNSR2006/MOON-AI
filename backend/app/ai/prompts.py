from typing import List, Optional

from app.ai.conversation import Conversation
from app.ai.models import ChatMessage


def build_chat_messages(conversation: Conversation, memories: Optional[List[str]] = None) -> List[dict]:
    messages: List[dict] = []
    if conversation.system_prompt:
        messages.append({"role": "system", "content": conversation.system_prompt})
    if memories:
        memory_content = "Relevant memories:\n" + "\n".join(memories)
        messages.append({"role": "system", "content": memory_content})
    for chat_message in conversation.get_history():
        messages.append({"role": chat_message.role, "content": chat_message.content})
    return messages
