from fastapi import WebSocket, WebSocketDisconnect
from app.services.manager import manager
from app.services.authorization import verify_ws_token


async def handle_websocket(websocket: WebSocket, batch_id: int):
    user = await verify_ws_token(websocket)
    if not user:
        return

    await websocket.accept()
    await manager.connect(batch_id, websocket)

    # Send identity to client
    await websocket.send_json(
        {
            "type": "init",
            "user_id": user["user_id"],
            "role": user["role"],
            "name": user["name"],
        }
    )

    try:
        while True:
            data = await websocket.receive_json()

            await manager.broadcast(
                batch_id,
                {
                    "type": "message",
                    "from_user_id": user["user_id"],
                    "from_role": user["role"],
                    "message": data["message"],
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(batch_id, websocket)
