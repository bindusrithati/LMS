from fastapi import APIRouter, Depends, Query, Request, status
from typing import List

from app.models.admin_models import AdminEmailRequest
from app.models.base_response_model import ApiResponse, SuccessMessageResponse
from app.models.guest_models import GuestRequest, GetGuestResponse
from app.services.email_service import EmailService
from app.services.guest_service import GuestService


router = APIRouter(
    prefix="/admin",
    tags=["ADMIN MANAGEMENT SERVICE"],
)


@router.post(
    "/send-email",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
)
async def send_email(
    request_state: Request,
    request: AdminEmailRequest,
) -> ApiResponse[SuccessMessageResponse]:
    return EmailService.send_email(
        to_email=request.email,
        receiver_type=request.receiver_type,
    )
