from fastapi import APIRouter, Depends, status

from app.models.auth_models import (
    LoginRequest,
    LoginResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RegisterRequest,
)
from app.models.base_response_model import ApiResponse, SuccessMessageResponse
from app.services.auth_service import AuthService
from app.utils.rate_limiter import rate_limiter

from app.config import settings

router = APIRouter(tags=["AUTHENTICATION MANAGEMENT SERVICE"])


# ---------------- LOGIN (RATE LIMITED) ----------------
@router.post(
    "/login",
    response_model=ApiResponse[LoginResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter("auth:login", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(AuthService),
):
    return ApiResponse(data=service.login(request))


# ---------------- FORGOT PASSWORD (RATE LIMITED) ----------------
@router.post(
    "/forgot-password",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter("auth:forgot-password", settings.RATE_LIMIT_SENSITIVE, settings.RATE_LIMIT_WINDOW))],
)
async def forgot_password(
    request: ForgotPasswordRequest,
    service: AuthService = Depends(AuthService),
):
    return ApiResponse(data=service.forgot_password(request.email))


# ---------------- RESET PASSWORD (RATE LIMITED) ----------------
@router.post(
    "/reset-password",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter("auth:reset-password", settings.RATE_LIMIT_SENSITIVE, settings.RATE_LIMIT_WINDOW))],
)
async def reset_password(
    request: ResetPasswordRequest,
    service: AuthService = Depends(AuthService),
):
    return ApiResponse(
        data=service.reset_password(
            token=request.token,
            new_password=request.new_password,
        )
    )


@router.post(
    "/register",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter("auth:register", settings.RATE_LIMIT_SENSITIVE, settings.RATE_LIMIT_WINDOW))],
)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(AuthService),
):
    return ApiResponse(data=service.register(request))
