from typing import List
from fastapi import APIRouter, Depends, Request, status
from pydantic import PositiveInt

from app.models.base_response_model import ApiResponse, SuccessMessageResponse
from app.models.syllabus_models import GetSyllabusResponse, SyllabusRequest
from app.services.syllabus_service import SyllabusService
from app.utils.rate_limiter import rate_limiter
from app.config import settings

router = APIRouter(prefix="/syllabus", tags=["SYLLABUS MANAGEMENT SERVICE"])


# ---------------- CREATE SYLLABUS (RATE LIMITED) ----------------
@router.post(
    "",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new syllabus",
    dependencies=[Depends(rate_limiter("syllabus:create", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def create_syllabus(
    request_state: Request,
    request: SyllabusRequest,
    service: SyllabusService = Depends(SyllabusService),
) -> ApiResponse[SuccessMessageResponse]:
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.create_syllabus(request, logged_in_user_id))


# ---------------- GET ALL SYLLABUS (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "",
    response_model=ApiResponse[List[GetSyllabusResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all syllabus",
)
async def get_all_syllabus(
    service: SyllabusService = Depends(SyllabusService),
) -> ApiResponse[List[GetSyllabusResponse]]:
    return ApiResponse(data=await service.get_all_syllabus())


# ---------------- GET SYLLABUS BY ID (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "/{syllabus_id}",
    response_model=ApiResponse[GetSyllabusResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve syllabus by id",
)
async def get_syllabus_by_id(
    syllabus_id: PositiveInt,
    service: SyllabusService = Depends(SyllabusService),
) -> ApiResponse[GetSyllabusResponse]:
    return ApiResponse(data=await service.get_syllabus_by_id(syllabus_id))


# ---------------- UPDATE SYLLABUS (RATE LIMITED) ----------------
@router.put(
    "/{syllabus_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Update syllabus by id",
    dependencies=[Depends(rate_limiter("syllabus:update", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def update_syllabus_by_id(
    request_state: Request,
    syllabus_id: PositiveInt,
    request: SyllabusRequest,
    service: SyllabusService = Depends(SyllabusService),
) -> ApiResponse[SuccessMessageResponse]:
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(
        data=service.update_syllabus_by_id(syllabus_id, request, logged_in_user_id)
    )


# ---------------- DELETE SYLLABUS (RATE LIMITED) ----------------
@router.delete(
    "/{syllabus_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete syllabus by id",
    dependencies=[Depends(rate_limiter("syllabus:delete", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def delete_syllabus_by_id(
    syllabus_id: PositiveInt,
    service: SyllabusService = Depends(SyllabusService),
) -> ApiResponse[SuccessMessageResponse]:
    return ApiResponse(data=service.delete_syllabus_by_id(syllabus_id))
