import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.ai.manager import ai_manager
from app.schemas.chat import ChatRequest
from app.websocket.manager import ConnectionManager
from app.core.logger import logger

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/chat")
async def chat_socket(websocket: WebSocket):
    client_info = websocket.client
    client_id = client_info[0] if client_info else "anonymous"
    await manager.connect(websocket, client_id)
    logger.info("WebSocket client connected: %s", client_id)
    try:
        while True:
            raw_data = await websocket.receive_text()
            logger.info("WebSocket received message from %s", client_id)
            try:
                payload = json.loads(raw_data)
                request = ChatRequest(**payload)
            except Exception as error:
                await websocket.send_text(json.dumps({"error": str(error)}))
                continue

            try:
                async for chunk in await ai_manager.stream(request):
                    await websocket.send_text(chunk)
            except Exception as error:
                await websocket.send_text(json.dumps({"error": str(error)}))
                break
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info("WebSocket client disconnected: %s", client_id)
