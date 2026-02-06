# app/ws_chat.py
from datetime import datetime
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.authorization import verify_ws_token
from app.services.manager import manager
from app.connectors.database_connector import get_database
from app.entities.chat import ChatMessage


router = APIRouter(tags=["BATCH CHAT"])


@router.websocket("/ws/chat/batch/{batch_id}")
async def batch_chat(websocket: WebSocket, batch_id: int):
    user = await verify_ws_token(websocket)

    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(batch_id, websocket)

    # Init payload
    await websocket.send_json(
        {
            "type": "init",
            "user_id": user["user_id"],
            "user_name": user["name"],
            "user_role": user["role"],
        }
    )

    try:
        while True:
            data = await websocket.receive_json()

            message_text = data.get("message")
            if not message_text:
                continue
            
            # Save message to database
            db = get_database()
            new_message = ChatMessage(
                batch_id=batch_id,
                user_id=user["user_id"],
                message=message_text,
                timestamp=datetime.now()
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            db.close()

            await manager.broadcast(
                batch_id,
                {
                    "type": "message",
                    "id": str(uuid.uuid4()),
                    "batch_id": batch_id,
                    "user_id": user["user_id"],
                    "user_name": user["name"],
                    "user_role": user["role"],
                    "message": message_text,
                    "timestamp": datetime.now().isoformat(),
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(batch_id, websocket)

        await manager.broadcast(
            batch_id,
            {
                "type": "leave",
                "user_id": user["user_id"],
                "user_name": user["name"],
                "timestamp": datetime.now().isoformat(),
            },
        )
