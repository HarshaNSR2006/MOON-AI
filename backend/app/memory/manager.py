from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.ai.exceptions import AIProviderUnavailable
from app.core.config import settings
from app.memory.chroma_store import ChromaStore
from app.memory.embeddings import EmbeddingGenerator
from app.memory.models import MemoryCreate, MemoryResponse, MemorySearchRequest, MemorySearchResult
from app.memory.retrieval import MemoryRetriever
from app.memory.storage import MemoryStorage


class MemoryManager:
    def __init__(
        self,
        storage: Optional[MemoryStorage] = None,
        store: Optional[ChromaStore] = None,
        retriever: Optional[MemoryRetriever] = None,
        embeddings: Optional[EmbeddingGenerator] = None,
    ) -> None:
        self.storage = storage or MemoryStorage()
        self.embedding_generator = embeddings or EmbeddingGenerator()
        self.store = store
        self.retriever = retriever

        if self.store is None:
            try:
                self.store = ChromaStore()
            except AIProviderUnavailable:
                self.store = None

        if self.store is not None and self.retriever is None:
            self.retriever = MemoryRetriever(self.store, self.embedding_generator)

    async def save_memory(
        self,
        memory_create: MemoryCreate,
    ) -> MemoryResponse:
        memory = self.storage.save_memory(
            content=memory_create.content,
            category=memory_create.category,
            importance=memory_create.importance,
            conversation_id=memory_create.conversation_id,
            metadata=memory_create.metadata,
        )
        if self.store is not None:
            embedding = await self.embedding_generator.embed_text(memory.content)
            self.store.add_memory(
                memory_id=memory.id,
                content=memory.content,
                metadata={
                    "category": memory.category,
                    "importance": memory.importance,
                    "conversation_id": memory.conversation_id,
                    "timestamp": memory.timestamp.isoformat(),
                    **(memory.metadata_json or {}),
                },
                embedding=embedding,
            )
        return MemoryResponse(
            id=memory.id,
            content=memory.content,
            category=memory.category,
            importance=memory.importance,
            timestamp=memory.timestamp,
            conversation_id=memory.conversation_id,
            metadata=memory.metadata_json,
        )

    async def search_memories(
        self,
        search_request: MemorySearchRequest,
    ) -> List[MemorySearchResult]:
        if self.retriever is None:
            raise AIProviderUnavailable("Memory search is not available because the vector store is not configured.")
        return await self.retriever.retrieve(
            query=search_request.query,
            top_k=search_request.top_k or settings.memory_top_k,
            conversation_id=search_request.conversation_id,
            category=search_request.category,
        )

    def list_memories(
        self,
        conversation_id: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[MemoryResponse]:
        items = self.storage.list_memories(conversation_id=conversation_id, category=category)
        return [
            MemoryResponse(
                id=item.id,
                content=item.content,
                category=item.category,
                importance=item.importance,
                timestamp=item.timestamp,
                conversation_id=item.conversation_id,
                metadata=item.metadata,
            )
            for item in items
        ]

    def delete_memory(self, memory_id: str) -> bool:
        deleted = self.storage.delete_memory(memory_id)
        if deleted:
            self.store.delete_memory(memory_id)
        return deleted

    async def update_memory(
        self,
        memory_id: str,
        memory_update: dict[str, Any],
    ) -> Optional[MemoryResponse]:
        memory = self.storage.update_memory(
            memory_id=memory_id,
            content=memory_update.get("content"),
            category=memory_update.get("category"),
            importance=memory_update.get("importance"),
            metadata=memory_update.get("metadata"),
        )
        if memory is None:
            return None
        if self.store is not None:
            embedding = await self.embedding_generator.embed_text(memory.content)
            self.store.update_memory(
                memory_id=memory.id,
                content=memory.content,
                metadata={
                    "category": memory.category,
                    "importance": memory.importance,
                    "conversation_id": memory.conversation_id,
                    "timestamp": memory.timestamp.isoformat(),
                    **(memory.metadata_json or {}),
                },
                embedding=embedding,
            )
        return MemoryResponse(
            id=memory.id,
            content=memory.content,
            category=memory.category,
            importance=memory.importance,
            timestamp=memory.timestamp,
            conversation_id=memory.conversation_id,
            metadata=memory.metadata_json,
        )

    def get_conversation_history(self, conversation_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        messages = self.storage.get_conversation_history(conversation_id, limit=limit)
        return [
            {
                "role": message.role,
                "content": message.content,
                "timestamp": message.created_at,
            }
            for message in messages
        ]

    async def retrieve_relevant_memories(
        self,
        conversation_id: str,
        query: str,
        top_k: Optional[int] = None,
    ) -> List[MemoryResponse]:
        search_request = MemorySearchRequest(
            query=query,
            conversation_id=conversation_id,
            top_k=top_k or settings.memory_top_k,
        )
        results = await self.search_memories(search_request)
        return [
            MemoryResponse(
                id=item.id,
                content=item.content,
                category=item.category,
                importance=item.importance,
                timestamp=item.timestamp,
                conversation_id=item.conversation_id,
                metadata=item.metadata,
            )
            for item in results
        ]


memory_manager = MemoryManager()
