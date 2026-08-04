from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.memory.manager import memory_manager
from app.memory.models import (
    ConversationHistoryResponse,
    MemoryCreate,
    MemoryResponse,
    MemorySearchRequest,
    MemorySearchResult,
    MemoryUpdate,
)

router = APIRouter()


@router.post("/save", response_model=MemoryResponse)
async def save_memory(
    payload: MemoryCreate,
    current_user=Depends(get_current_user),
) -> MemoryResponse:
    return await memory_manager.save_memory(payload)


@router.post("/search", response_model=list[MemorySearchResult])
async def search_memory(
    payload: MemorySearchRequest,
    current_user=Depends(get_current_user),
) -> list[MemorySearchResult]:
    return await memory_manager.search_memories(payload)


@router.get("/list", response_model=list[MemoryResponse])
def list_memories(
    conversation_id: Optional[str] = None,
    category: Optional[str] = None,
    current_user=Depends(get_current_user),
) -> list[MemoryResponse]:
    return memory_manager.list_memories(conversation_id=conversation_id, category=category)


@router.delete("/{memory_id}")
def delete_memory(
    memory_id: str,
    current_user=Depends(get_current_user),
) -> dict[str, bool]:
    deleted = memory_manager.delete_memory(memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"deleted": True}


@router.patch("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: str,
    payload: MemoryUpdate,
    current_user=Depends(get_current_user),
) -> MemoryResponse:
    memory = await memory_manager.update_memory(memory_id, payload.model_dump(exclude_none=True))
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


@router.get("/conversations/{conversation_id}", response_model=ConversationHistoryResponse)
def get_conversation_history(
    conversation_id: str,
    current_user=Depends(get_current_user),
) -> ConversationHistoryResponse:
    messages = memory_manager.get_conversation_history(conversation_id)
    return ConversationHistoryResponse(conversation_id=conversation_id, messages=messages)
