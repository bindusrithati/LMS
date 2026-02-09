from typing import List
from unittest import result
from fastapi import APIRouter, Depends, Request, status
from pydantic import PositiveInt

from app.models.base_response_model import (
    ApiResponse,
    CreateResponse,
    SuccessMessageResponse,
)
from app.models.batch_models import (
    BatchRequest,
    ClassScheduleRequest,
    GetBatchResponse,
    GetClassScheduleResponse,
    UpdateClassScheduleRequest,
    GetChatMessageResponse,
)
from app.services.batch_service import BatchService
from app.utils.rate_limiter import rate_limiter
from app.config import settings

router = APIRouter(prefix="/batches", tags=["BATCH MANAGEMENT SERVICE"])


# ---------------- CREATE BATCH (RATE LIMITED) ----------------
@router.post(
    "",
    response_model=ApiResponse[CreateResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new batch",
    dependencies=[Depends(rate_limiter("batch:create", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def create_batch(
    request_state: Request,
    request: BatchRequest,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[CreateResponse]:
    logged_in_user_id = request_state.state.user.id
    result = await service.create_batch(request, logged_in_user_id)
    return ApiResponse(data=result)


# ---------------- GET ALL BATCHES (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "",
    response_model=ApiResponse[List[GetBatchResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all batches",
)
async def get_all_batches(
    service: BatchService = Depends(BatchService),
):
    data = await service.get_all_batches()  # 🔥 MUST await
    return ApiResponse(data=data)


# ---------------- GET BATCH BY ID (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "/{batch_id}",
    response_model=ApiResponse[GetBatchResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve batch by id",
)
async def get_batch_by_id(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[GetBatchResponse]:
    return ApiResponse(data=await service.get_batch_by_id(batch_id))


# ---------------- UPDATE BATCH (RATE LIMITED) ----------------
@router.put(
    "/{batch_id}",
    response_model=ApiResponse[CreateResponse],
    status_code=status.HTTP_200_OK,
    summary="Update batch by id",
    dependencies=[Depends(rate_limiter("batch:update", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def update_batch_by_id(
    request_state: Request,
    batch_id: PositiveInt,
    request: BatchRequest,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[CreateResponse]:
    logged_in_user_id = request_state.state.user.id

    result = service.update_batch_by_id(batch_id, request, logged_in_user_id)
    return ApiResponse(data=result)


# ---------------- DELETE BATCH (RATE LIMITED) ----------------
@router.delete(
    "/{batch_id}",
    response_model=ApiResponse[CreateResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete batch by id",
    dependencies=[Depends(rate_limiter("batch:delete", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def delete_batch_by_id(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[CreateResponse]:
    return ApiResponse(data=service.delete_batch_by_id(batch_id))


# ---------------- CREATE CLASS SCHEDULE (RATE LIMITED) ----------------
@router.post(
    "/{batch_id}/schedule-class",
    response_model=ApiResponse[CreateResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter("batch:schedule:create", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def create_class_schedule(
    batch_id: PositiveInt,
    request: ClassScheduleRequest,
    request_state: Request,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[CreateResponse]:
    user_id = request_state.state.user.id
    return ApiResponse(data=service.create_schedule(batch_id, request, user_id))


# ---------------- GET CLASS SCHEDULES (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "/{batch_id}/schedule-class",
    response_model=ApiResponse[List[GetClassScheduleResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_class_schedules_by_batch(
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[List[GetClassScheduleResponse]]:
    return ApiResponse(data=await service.get_schedules_by_batch(batch_id))


# ---------------- UPDATE CLASS SCHEDULE (RATE LIMITED) ----------------
@router.put(
    "/{batch_id}/schedule-class/{schedule_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter("batch:schedule:update", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def update_class_schedule_by_id(
    schedule_id: PositiveInt,
    batch_id: PositiveInt,
    request: UpdateClassScheduleRequest,
    request_state: Request,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[SuccessMessageResponse]:

    user_id = request_state.state.user.id

    result = await service.update_schedule_by_id(
        schedule_id, batch_id, request, user_id
    )

    return ApiResponse(data=result)


# ---------------- DELETE CLASS SCHEDULE (RATE LIMITED) ----------------
@router.delete(
    "/{batch_id}/schedule-class/{schedule_id}",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter("batch:schedule:delete", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def delete_class_schedule_by_id(
    schedule_id: PositiveInt,
    batch_id: PositiveInt,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[SuccessMessageResponse]:
    return ApiResponse(data=service.delete_schedule_by_id(schedule_id, batch_id))



# ---------------- GET CHAT HISTORY ----------------
@router.get(
    "/{batch_id}/chats",
    response_model=ApiResponse[List[GetChatMessageResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve chat history for a batch",
)
async def get_batch_chat_history(
    batch_id: PositiveInt,
    request_state: Request,
    service: BatchService = Depends(BatchService),
) -> ApiResponse[List[GetChatMessageResponse]]:
    return ApiResponse(data=service.get_chat_history(batch_id, request_state.state.user))
