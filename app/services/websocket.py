from fastapi import WebSocket, WebSocketDisconnect
from app.services import manager
from app.services.authorization import verify_ws_token


async def handle_websocket(websocket: WebSocket, batch_id: int):
    user = await verify_ws_token(websocket)

    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(batch_id, websocket)

    await websocket.send_json(
        {
            "type": "init",
            "user_id": user["user_id"],
            "name": user["name"],
            "role": user["role"],
        }
    )

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            if not message:
                continue

            await manager.broadcast(
                batch_id,
                {
                    "type": "message",
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "role": user["role"],
                    "message": message,
                },
            )

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        manager.disconnect(batch_id, websocket)

        await manager.broadcast(
            batch_id,
            {
                "type": "leave",
                "user_id": user["user_id"],
            },
        )
