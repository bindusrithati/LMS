from typing import List

from fastapi import APIRouter, Depends, Request, status
from pydantic import PositiveInt

from app.models.base_response_model import ApiResponse, SuccessMessageResponse
from app.models.student_models import (
    GetMappedBatchStudentResponse,
    MapStudentToBatchRequest,
    StudentRequest,
    GetStudentResponse,
    UpdatedBatchStudentRequest,
)
from app.services.student_service import StudentService
from app.utils.rate_limiter import rate_limiter
from app.config import settings

router = APIRouter(prefix="/students", tags=["STUDENT MANAGEMENT SERVICE"])


# ---------------- CREATE STUDENT (RATE LIMITED) ----------------
@router.post(
    "",
    response_model=ApiResponse[SuccessMessageResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
    dependencies=[Depends(rate_limiter("students:create", settings.RATE_LIMIT_STANDARD, settings.RATE_LIMIT_WINDOW))],
)
async def create_student(
    request_state: Request,
    request: StudentRequest,
    service: StudentService = Depends(StudentService),
) -> ApiResponse[SuccessMessageResponse]:
    logged_in_user_id = request_state.state.user.id
    return ApiResponse(data=service.create_student(request, logged_in_user_id))


# ---------------- GET ALL STUDENTS (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "",
    response_model=ApiResponse[List[GetStudentResponse]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all students",
)
async def get_all_students(
    service: StudentService = Depends(StudentService),
) -> ApiResponse[List[GetStudentResponse]]:

    data = await service.get_all_students()  # ✅ await
    return ApiResponse(data=data)


# ---------------- GET STUDENT BY ID (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "/{student_id}",
    response_model=ApiResponse[GetStudentResponse],
)
async def get_student_by_id(
    student_id: PositiveInt,
    service: StudentService = Depends(StudentService),
):
    data = await service.get_student_by_id(student_id)
    return ApiResponse(data=data)


# ---------------- UPDATE STUDENT (RATE LIMITED) ----------------
@router.put(
    "/{student_id}",
    response_model=ApiResponse[SuccessMessageResponse],
)
async def update_student_by_id(
    request_state: Request,
    student_id: PositiveInt,
    request: StudentRequest,
    service: StudentService = Depends(StudentService),
):
    user_id = request_state.state.user.id
    data = await service.update_student_by_id(student_id, request, user_id)
    return ApiResponse(data=data)


# ---------------- DELETE STUDENT (RATE LIMITED) ----------------
@router.delete(
    "/{student_id}",
    response_model=ApiResponse[SuccessMessageResponse],
)
async def delete_student_by_id(
    student_id: PositiveInt,
    service: StudentService = Depends(StudentService),
):
    data = await service.delete_student_by_id(student_id)
    return ApiResponse(data=data)


# ---------------- MAP STUDENT TO BATCH (RATE LIMITED) ----------------
@router.post(
    "/{student_id}/batches",
    response_model=ApiResponse[SuccessMessageResponse],
)
async def map_student_to_batch(
    student_id: PositiveInt,
    request_state: Request,
    request: MapStudentToBatchRequest,
    service: StudentService = Depends(StudentService),
):
    user_id = request_state.state.user.id
    data = await service.map_student_to_batch(student_id, request, user_id)
    return ApiResponse(data=data)


# ---------------- GET BATCH STUDENTS (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "/batches/{batch_id}",
    response_model=ApiResponse[List[GetMappedBatchStudentResponse]],
)
async def get_batch_students(
    batch_id: PositiveInt,
    service: StudentService = Depends(StudentService),
):
    data = await service.get_batch_students(batch_id)
    return ApiResponse(data=data)


# ---------------- GET BATCH STUDENT BY ID (NO RATE LIMIT – CACHED) ----------------
@router.get(
    "/mappings/{mapping_id}",
    response_model=ApiResponse[GetMappedBatchStudentResponse],
)
async def get_batch_student_by_id(
    mapping_id: PositiveInt,
    service: StudentService = Depends(StudentService),
):
    data = await service.get_batch_student_by_id(mapping_id)
    return ApiResponse(data=data)


# ---------------- UPDATE BATCH STUDENT (RATE LIMITED) ----------------
@router.put(
    "/mappings/{mapping_id}",
    response_model=ApiResponse[SuccessMessageResponse],
)
async def update_batch_student_by_id(
    mapping_id: PositiveInt,
    request_state: Request,
    request: UpdatedBatchStudentRequest,
    service: StudentService = Depends(StudentService),
):
    user_id = request_state.state.user.id
    data = await service.update_batch_student_by_id(mapping_id, request, user_id)
    return ApiResponse(data=data)


# ---------------- DELETE BATCH STUDENT (RATE LIMITED) ----------------
@router.delete(
    "/mappings/{mapping_id}",
    response_model=ApiResponse[SuccessMessageResponse],
)
async def delete_batch_student_by_id(
    mapping_id: PositiveInt,
    service: StudentService = Depends(StudentService),
):
    data = await service.delete_batch_student_by_id(mapping_id)
    return ApiResponse(data=data)
