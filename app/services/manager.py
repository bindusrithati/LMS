from typing import Dict, List
from fastapi import WebSocket
from starlette.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}

    async def connect(self, batch_id: int, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(batch_id, []).append(websocket)

    def disconnect(self, batch_id: int, websocket: WebSocket):
        if batch_id in self.rooms and websocket in self.rooms[batch_id]:
            self.rooms[batch_id].remove(websocket)
            if not self.rooms[batch_id]:
                del self.rooms[batch_id]

    async def broadcast(self, batch_id: int, message: dict):
        for ws in self.rooms.get(batch_id, []).copy():
            if ws.application_state != WebSocketState.CONNECTED:
                self.disconnect(batch_id, ws)
                continue
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(batch_id, ws)


# ✅ SINGLE shared instance
manager = ConnectionManager()
