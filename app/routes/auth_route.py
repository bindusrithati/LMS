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

router = APIRouter(tags=["AUTHENTICATION MANAGEMENT SERVICE"])


# ---------------- LOGIN (RATE LIMITED) ----------------
@router.post(
    "/login",
    response_model=ApiResponse[LoginResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter("auth:login", 5, 60))],
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
    dependencies=[Depends(rate_limiter("auth:forgot-password", 3, 60))],
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
    dependencies=[Depends(rate_limiter("auth:reset-password", 3, 60))],
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
    dependencies=[Depends(rate_limiter("auth:register", 3, 60))],
)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(AuthService),
):
    return ApiResponse(data=service.register(request))
