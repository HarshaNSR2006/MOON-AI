import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.database.models import Conversation, ConversationMessage, MemoryItem
from app.database.session import SessionLocal


class MemoryStorage:
    def __init__(self, session_factory=SessionLocal) -> None:
        self.session_factory = session_factory

    def _create_conversation(self, db: Session, conversation_id: str, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(id=conversation_id, title=title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def ensure_conversation_exists(self, conversation_id: str, title: Optional[str] = None) -> Conversation:
        with self.session_factory() as db:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conversation is None:
                conversation = self._create_conversation(db, conversation_id, title)
            return conversation

    def save_conversation_message(self, conversation_id: str, role: str, content: str) -> None:
        with self.session_factory() as db:
            self.ensure_conversation_exists(conversation_id)
            message = ConversationMessage(conversation_id=conversation_id, role=role, content=content)
            db.add(message)
            db.commit()

    def get_conversation_history(self, conversation_id: str, limit: Optional[int] = None) -> List[ConversationMessage]:
        with self.session_factory() as db:
            query = db.query(ConversationMessage).filter(ConversationMessage.conversation_id == conversation_id).order_by(ConversationMessage.created_at.asc())
            if limit:
                query = query.limit(limit)
            return query.all()

    def save_memory(
        self,
        content: str,
        category: str,
        importance: float,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        with self.session_factory() as db:
            memory = MemoryItem(
                id=uuid.uuid4().hex,
                content=content,
                category=category,
                importance=importance,
                conversation_id=conversation_id,
                metadata_json=metadata,
            )
            db.add(memory)
            db.commit()
            db.refresh(memory)
            return memory

    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        with self.session_factory() as db:
            return db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        category: Optional[str] = None,
        importance: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[MemoryItem]:
        with self.session_factory() as db:
            memory = db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()
            if memory is None:
                return None
            if content is not None:
                memory.content = content
            if category is not None:
                memory.category = category
            if importance is not None:
                memory.importance = importance
            if metadata is not None:
                memory.metadata_json = metadata
            db.commit()
            db.refresh(memory)
            return memory

    def delete_memory(self, memory_id: str) -> bool:
        with self.session_factory() as db:
            memory = db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()
            if memory is None:
                return False
            db.delete(memory)
            db.commit()
            return True

    def list_memories(
        self,
        conversation_id: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
    ) -> List[MemoryItem]:
        with self.session_factory() as db:
            query = db.query(MemoryItem)
            if conversation_id is not None:
                query = query.filter(MemoryItem.conversation_id == conversation_id)
            if category is not None:
                query = query.filter(MemoryItem.category == category)
            return query.order_by(MemoryItem.timestamp.desc()).limit(limit).all()
