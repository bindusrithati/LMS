from fastapi import APIRouter, Depends, status
from typing import List

from app.models.base_response_model import ApiResponse, SuccessMessageResponse
from app.models.guest_models import GuestRequest, GetGuestResponse
from app.services.guest_service import GuestService


router = APIRouter(
    prefix="/guests",
    tags=["GUEST MANAGEMENT SERVICE"],
)


# ---------------- CREATE GUEST (PUBLIC) ----------------
@router.post(
    "",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_guest(
    request: GuestRequest,
    service: GuestService = Depends(GuestService),
):
    data = service.create_guest(request)
    return ApiResponse(data=data)


# ---------------- GET ALL GUESTS ----------------
@router.get(
    "",
    response_model=ApiResponse[List[GetGuestResponse]],
)
async def get_all_guests(
    service: GuestService = Depends(GuestService),
):
    data = service.get_all_guests()
    return ApiResponse(data=data)


# ---------------- GET GUEST BY ID ----------------
@router.get(
    "/{guest_id}",
    response_model=ApiResponse[GetGuestResponse],
)
async def get_guest_by_id(
    guest_id: int,
    service: GuestService = Depends(GuestService),
):
    data = service.get_guest_by_id(guest_id)
    return ApiResponse(data=data)
