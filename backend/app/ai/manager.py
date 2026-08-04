from typing import AsyncGenerator, Dict, List, Optional

from app.ai.context import ContextManager
from app.ai.exceptions import (
    AIProviderUnavailable,
    InvalidModel,
    StreamingError,
)
from app.ai.models import AIRequest, AIResponse
from app.ai.prompts import build_chat_messages
from app.core.config import settings
from app.memory.manager import memory_manager
from app.providers.openai_provider import OpenAIProvider
from app.providers.ollama_provider import OllamaProvider


class AIManager:
    def __init__(self, providers: Optional[List] = None) -> None:
        provider_instances = providers or [OpenAIProvider(), OllamaProvider()]
        self.providers: Dict[str, object] = {p.name: p for p in provider_instances}
        self.default_provider = settings.default_provider
        self.default_model = settings.default_model
        self.context_manager = ContextManager()

    def get_provider(self, provider_name: Optional[str] = None):
        provider_name = provider_name or self.default_provider
        if provider_name not in self.providers:
            raise AIProviderUnavailable(f"Provider '{provider_name}' is not available.")
        return self.providers[provider_name]

    async def available_models(self, provider_name: Optional[str] = None) -> List[str]:
        provider = self.get_provider(provider_name)
        return await provider.available_models()

    def select_provider(self, provider_name: str) -> None:
        if provider_name not in self.providers:
            raise AIProviderUnavailable(f"Provider '{provider_name}' is not available.")
        self.default_provider = provider_name

    async def generate(self, request: AIRequest) -> AIResponse:
        provider = self.get_provider(request.provider)
        model = request.model or self.default_model
        temperature = request.temperature if request.temperature is not None else settings.temperature

        conversation = self.context_manager.get_conversation(request.conversation_id)
        conversation.add_user_message(request.message)
        memories: list[str] = []
        try:
            memory_results = await memory_manager.retrieve_relevant_memories(
                conversation_id=request.conversation_id,
                query=request.message,
                top_k=settings.memory_top_k,
            )
            memories = [f"- {memory.content}" for memory in memory_results]
        except AIProviderUnavailable:
            memories = []
        messages = build_chat_messages(conversation, memories=memories)

        try:
            text = await provider.generate(messages=messages, model=model, temperature=temperature)
        except Exception as exc:
            raise AIProviderUnavailable(str(exc)) from exc

        conversation.add_assistant_message(text)
        memory_manager.storage.save_conversation_message(request.conversation_id, "user", request.message)
        memory_manager.storage.save_conversation_message(request.conversation_id, "assistant", text)

        return AIResponse(
            conversation_id=request.conversation_id,
            response=text,
            provider=provider.name,
            model=model,
        )

    async def stream(self, request: AIRequest) -> AsyncGenerator[str, None]:
        provider = self.get_provider(request.provider)
        model = request.model or self.default_model
        temperature = request.temperature if request.temperature is not None else settings.temperature

        conversation = self.context_manager.get_conversation(request.conversation_id)
        conversation.add_user_message(request.message)
        memories: list[str] = []
        try:
            memory_results = await memory_manager.retrieve_relevant_memories(
                conversation_id=request.conversation_id,
                query=request.message,
                top_k=settings.memory_top_k,
            )
            memories = [f"- {memory.content}" for memory in memory_results]
        except AIProviderUnavailable:
            memories = []
        messages = build_chat_messages(conversation, memories=memories)

        if not hasattr(provider, "stream"):
            raise StreamingError(f"Provider '{provider.name}' does not support streaming.")

        async def stream_generator() -> AsyncGenerator[str, None]:
            buffer = ""
            try:
                async for chunk in provider.stream(messages=messages, model=model, temperature=temperature):
                    buffer += chunk
                    yield chunk
            except Exception as exc:
                raise StreamingError(str(exc)) from exc
            conversation.add_assistant_message(buffer)
            memory_manager.storage.save_conversation_message(request.conversation_id, "user", request.message)
            memory_manager.storage.save_conversation_message(request.conversation_id, "assistant", buffer)
 
        return stream_generator()


ai_manager = AIManager()
