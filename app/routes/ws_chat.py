# app/ws_chat.py
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import time

router = APIRouter(prefix="/ws_chat", tags=["BATCH MANAGEMENT SERVICE"])


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}

    async def connect(self, batch_id: int, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(batch_id, []).append(websocket)

    def disconnect(self, batch_id: int, websocket: WebSocket):
        self.rooms[batch_id].remove(websocket)

    async def broadcast(self, batch_id: int, message: dict):
        for ws in self.rooms.get(batch_id, []):
            await ws.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/batch/{batch_id}")
async def batch_chat(websocket: WebSocket, batch_id: int):
    client_id = int(time.time() * 1000)

    await manager.connect(batch_id, websocket)

    # 🔥 SEND CLIENT ID ONLY TO THIS CLIENT
    await websocket.send_json({"type": "init", "client_id": client_id})

    try:
        while True:
            data = await websocket.receive_json()

            await manager.broadcast(
                batch_id,
                {
                    "type": "message",
                    "client_id": client_id,
                    "message": data["message"],
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(batch_id, websocket)
