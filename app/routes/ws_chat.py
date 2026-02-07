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

    # ---------------- AUTHORIZATION CHECK ----------------
    db = get_database()
    is_authorized = False
    try:
        user_role = user.get("role")
        user_id = user.get("user_id")

        if user_role in ["Admin", "SuperAdmin"]:
            is_authorized = True
        
        elif user_role == "Mentor":
            from app.entities.batch import Batch
            # Check if this mentor is assigned to the batch
            batch = db.query(Batch).filter(Batch.id == batch_id, Batch.mentor == user_id).first()
            if batch:
                is_authorized = True
        
        elif user_role == "Student":
            from app.entities.student import Student
            from app.entities.batch_student import BatchStudent
            # Get student profile
            student = db.query(Student).filter(Student.user_id == user_id).first()
            if student:
                # Check enrollment
                enrollment = db.query(BatchStudent).filter(
                    BatchStudent.batch_id == batch_id,
                    BatchStudent.student_id == student.id
                ).first()
                if enrollment:
                    is_authorized = True

        if not is_authorized:
            print(f"Unauthorized chat access: User {user_id} ({user_role}) -> Batch {batch_id}")
            db.close()
            await websocket.close(code=1008)
            return

    except Exception as e:
        print(f"Chat Auth Error: {e}")
        db.close()
        await websocket.close(code=1011)
        return
    
    db.close()
    # -----------------------------------------------------

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
