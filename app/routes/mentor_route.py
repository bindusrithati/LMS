from fastapi import APIRouter, Depends, Request, status

from app.models.base_response_model import ApiResponse, SuccessMessageResponse
from app.models.mentor_models import (
    MentorProfileRequest,
    GetMentorProfileResponse,
)
from app.services.mentor_service import MentorService
from app.utils.rate_limiter import rate_limiter
from app.config import settings

router = APIRouter(
    prefix="/mentors",
    tags=["MENTOR MANAGEMENT SERVICE"],
)


# ---------------- CREATE MENTOR PROFILE (RATE LIMITED) ----------------
@router.post(
    "/profile",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter("mentors:create", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def create_mentor_profile(
    request_state: Request,
    request: MentorProfileRequest,
    service: MentorService = Depends(MentorService),
) -> ApiResponse[SuccessMessageResponse]:

    logged_in_user_id = request_state.state.user.id
    data = service.create_mentor_profile(request, logged_in_user_id)
    return ApiResponse(data=data)


# ---------------- GET MENTOR PROFILE BY USER ID ----------------
@router.get(
    "/profile/{user_id}",
    response_model=ApiResponse[GetMentorProfileResponse],
    status_code=status.HTTP_200_OK,
)
async def get_mentor_profile(
    user_id: int,
    service: MentorService = Depends(MentorService),
) -> ApiResponse[GetMentorProfileResponse]:

    data = service.get_mentor_profile_by_user_id(user_id)
    return ApiResponse(data=data)
