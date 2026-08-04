import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.ai.exceptions import AIProviderUnavailable, InvalidModel, StreamingError
from app.ai.manager import ai_manager
from app.auth.dependencies import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ModelListResponse,
    ModelSelectionRequest,
    ModelSelectionResponse,
)

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def send_chat_message(
    payload: ChatRequest,
    current_user=Depends(get_current_user),
) -> ChatResponse:
    try:
        return await ai_manager.generate(payload)
    except AIProviderUnavailable as error:
        raise HTTPException(status_code=503, detail=str(error))
    except InvalidModel as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/stream")
async def stream_chat_message(
    payload: ChatRequest,
    current_user=Depends(get_current_user),
) -> StreamingResponse:
    async def event_generator():
        try:
            async for chunk in await ai_manager.stream(payload):
                event_data = json.dumps({"chunk": chunk})
                yield f"data: {event_data}\n\n"
        except AIProviderUnavailable as error:
            yield f"data: {json.dumps({'error': str(error)})}\n\n"
        except StreamingError as error:
            yield f"data: {json.dumps({'error': str(error)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/models", response_model=ModelListResponse)
async def list_models(provider: Optional[str] = None) -> ModelListResponse:
    provider_name = provider or ai_manager.default_provider
    try:
        models = await ai_manager.available_models(provider_name)
    except AIProviderUnavailable as error:
        raise HTTPException(status_code=503, detail=str(error))
    return ModelListResponse(provider=provider_name, models=models)


@router.post("/models/select", response_model=ModelSelectionResponse)
async def select_model(selection: ModelSelectionRequest) -> ModelSelectionResponse:
    try:
        ai_manager.select_provider(selection.provider)
    except AIProviderUnavailable as error:
        raise HTTPException(status_code=400, detail=str(error))
    ai_manager.default_model = selection.model
    return ModelSelectionResponse(provider=selection.provider, model=selection.model)
