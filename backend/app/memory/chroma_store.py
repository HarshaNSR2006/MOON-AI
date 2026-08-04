import os
from typing import Any, Dict, List, Optional

from app.ai.exceptions import AIProviderUnavailable
from app.core.config import settings

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
except ImportError:  # pragma: no cover
    chromadb = None


DEFAULT_COLLECTION = "memories"


class ChromaStore:
    def __init__(self) -> None:
        if chromadb is None:
            raise AIProviderUnavailable(
                "ChromaDB is not installed. Install chromadb to enable long-term memory."
            )

        self.path = settings.chroma_path
        os.makedirs(self.path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.path)
        self.collection = self.client.get_or_create_collection(name=DEFAULT_COLLECTION)

    def add_memory(
        self,
        memory_id: str,
        content: str,
        metadata: Dict[str, Any],
        embedding: List[float],
    ) -> None:
        self.collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata],
            embeddings=[embedding],
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["ids", "documents", "metadatas", "distances"],
            where=filter,
        )
        rows = []
        if results and results.get("ids"):
            ids = results["ids"][0]
            docs = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]
            for memory_id, content, metadata, distance in zip(ids, docs, metadatas, distances):
                rows.append(
                    {
                        "id": memory_id,
                        "content": content,
                        "metadata": metadata,
                        "similarity": 1.0 - distance if distance is not None else None,
                    }
                )
        return rows

    def delete_memory(self, memory_id: str) -> None:
        self.collection.delete(ids=[memory_id])

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        update_kwargs: Dict[str, Any] = {"ids": [memory_id]}
        if content is not None:
            update_kwargs["documents"] = [content]
        if metadata is not None:
            update_kwargs["metadatas"] = [metadata]
        if embedding is not None:
            update_kwargs["embeddings"] = [embedding]
        self.collection.update(**update_kwargs)
