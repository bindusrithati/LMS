from fastapi import APIRouter, WebSocket
from app.services.websocket import handle_websocket

router = APIRouter()


@router.websocket("/ws/chat/batch/{batch_id}")
async def chat_ws(websocket: WebSocket, batch_id: int):
    await handle_websocket(websocket, batch_id)
