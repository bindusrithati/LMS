import os
from dotenv import load_dotenv
from jose import jwt
from fastapi import Request, HTTPException, status
from app.models.user_models import CurrentContextUser
from app.utils.constants import AUTHORIZATION

load_dotenv()

SECRET_KEY: str = os.getenv("JWT_SECRET")  # type: ignore
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300  # 3 hours


def __verify_jwt(token: str):
    token = token.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_sub": True})  # type: ignore
    user_email = payload.get("email")

    if user_email:
        cur_user = CurrentContextUser()
        cur_user.id = payload.get("id")
        cur_user.name = str(user_email)
        cur_user.role = payload.get("role")
        return cur_user


async def verify_auth_token(request: Request):
    if "login" not in request.url.path and "refresh" not in request.url.path:
        auth: str = request.headers.get(AUTHORIZATION) or ""
        try:
            token = auth.strip()
            request.state.user = __verify_jwt(token=token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
