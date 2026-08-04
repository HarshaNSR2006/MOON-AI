from app.ai.context import ContextManager


def test_context_manager_trims_message_history() -> None:
    manager = ContextManager()
    conversation = manager.get_conversation("context-test")
    for index in range(30):
        conversation.add_user_message(f"user {index}")
        conversation.add_assistant_message(f"assistant {index}")

    manager.get_conversation("context-test")
    assert len(conversation.messages) <= manager.max_messages
    assert conversation.messages[0].content == "user 20"
