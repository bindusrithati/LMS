from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}

    async def connect(self, batch_id: int, websocket: WebSocket):
        if batch_id not in self.rooms:
            self.rooms[batch_id] = []
        self.rooms[batch_id].append(websocket)

    def disconnect(self, batch_id: int, websocket: WebSocket):
        self.rooms[batch_id].remove(websocket)
        if not self.rooms[batch_id]:
            del self.rooms[batch_id]

    async def broadcast(self, batch_id: int, message: dict):
        for ws in self.rooms.get(batch_id, []):
            await ws.send_json(message)


manager = ConnectionManager()
