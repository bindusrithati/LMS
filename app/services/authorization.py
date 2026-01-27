from jose import jwt, JWTError
from fastapi import WebSocket, status
from app.config import settings  # or where SECRET_KEY lives

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"


async def verify_ws_token(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload["id"],
            "role": payload["role"],
            "name": payload.get("name"),
        }
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
