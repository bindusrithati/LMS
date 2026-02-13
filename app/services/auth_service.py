from datetime import datetime, timedelta
from dataclasses import dataclass
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from app.models.base_response_model import SuccessMessageResponse
from app.entities.user import User

from app.entities.user import User
from app.models.auth_models import (
    LoginRequest,
    LoginResponse,
)
from .user_service import UserService
from app.services.email_service import EmailService


from app.utils.auth_dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from app.utils.constants import (
    INCORRECT_PASSWORD,
    USER_NOT_FOUND,
    INVALID_RESET_TOKEN,
    RESET_TOKEN_EXPIRED,
    PASSWORD_RESET_SUCCESSFULLY,
    PASSWORD_RESET_LINK_SENT,
    USER_ALREADY_EXISTS,
    USER_REGISTERED_SUCCESSFULLY,
)


RESET_TOKEN_EXPIRE_MINUTES = 15  # 👈 short expiry for security


@dataclass
class AuthService:
    user_service: UserService = Depends(UserService)

    # ---------------- JWT CLAIMS ----------------
    def create_claims(self, user: User):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "phone_number": user.phone_number,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

    def generate_token_response(self, claims: dict) -> LoginResponse:
        try:
            token = jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)
            return LoginResponse(access_token=token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    # ---------------- LOGIN ----------------
    def login(self, request: LoginRequest) -> LoginResponse:
        user = self.user_service.get_active_user_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=USER_NOT_FOUND,
            )

        if not user.verify_password(request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INCORRECT_PASSWORD,
            )

        claims = self.create_claims(user)
        return self.generate_token_response(claims=claims)

    # =========================================================
    # NEW: FORGOT PASSWORD
    # =========================================================

    def forgot_password(self, email: str):
        """
        Generate reset token and send email.
        """
        user = self.user_service.get_active_user_by_email(email)

        # SECURITY: always return success
        if not user:
            return SuccessMessageResponse(message=PASSWORD_RESET_LINK_SENT)

        reset_claims = {
            "sub": "password_reset",
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES),
        }

        reset_token = jwt.encode(
            claims=reset_claims,
            key=SECRET_KEY,
            algorithm=ALGORITHM,
        )

        # ✅ SEND EMAIL
        EmailService.send_reset_password_email(user.email, reset_token)

        return SuccessMessageResponse(message=PASSWORD_RESET_LINK_SENT)

    # =========================================================
    # NEW: RESET PASSWORD
    # =========================================================
    def reset_password(self, token: str, new_password: str):
        """
        Validate reset token and update password.
        """
        try:
            payload = jwt.decode(
                token,
                key=SECRET_KEY,
                algorithms=[ALGORITHM],
            )

            if payload.get("sub") != "password_reset":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=INVALID_RESET_TOKEN,
                )

            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=INVALID_RESET_TOKEN,
                )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=RESET_TOKEN_EXPIRED,
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_RESET_TOKEN,
            )

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=USER_NOT_FOUND,
            )

        # update password (hashed inside model/service)
        user.password = new_password
        self.user_service.update(user)

        return SuccessMessageResponse(message=PASSWORD_RESET_SUCCESSFULLY)

    def register(self, request):
        """
        Register a new user
        """
        existing_user = self.user_service.get_active_user_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=USER_ALREADY_EXISTS,
            )

        user = User(
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
        )

        # ✅ ENUM VALIDATION SHOULD BE HERE
        try:
            user.gender = request.gender.upper()  # MALE / FEMALE / OTHER
            user.role = request.role.capitalize()  # Admin / SuperAdmin

        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INVALID_GENDER_OR_ROLE",
            )

        # ✅ password hashing
        user.password = request.password

        # ✅ persist
        self.user_service.save(user)

        return SuccessMessageResponse(message=USER_REGISTERED_SUCCESSFULLY)
