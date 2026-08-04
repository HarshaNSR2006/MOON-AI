from typing import Any, Dict, List, Optional

from app.memory.chroma_store import ChromaStore
from app.memory.embeddings import EmbeddingGenerator
from app.memory.models import MemorySearchResult


class MemoryRetriever:
    def __init__(self, store: ChromaStore, embeddings: EmbeddingGenerator) -> None:
        self.store = store
        self.embeddings = embeddings

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        conversation_id: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[MemorySearchResult]:
        embedding = await self.embeddings.embed_text(query)
        filter: Optional[Dict[str, Any]] = None
        if conversation_id is not None or category is not None:
            filter = {}
            if conversation_id is not None:
                filter["conversation_id"] = conversation_id
            if category is not None:
                filter["category"] = category

        results = self.store.search(query_embedding=embedding, top_k=top_k, filter=filter)
        return [
            MemorySearchResult(
                id=item["id"],
                content=item["content"],
                category=item["metadata"].get("category", "general"),
                importance=float(item["metadata"].get("importance", 0.5)),
                timestamp=item["metadata"].get("timestamp"),
                conversation_id=item["metadata"].get("conversation_id"),
                metadata=item["metadata"],
                similarity=item["similarity"],
            )
            for item in results
        ]
