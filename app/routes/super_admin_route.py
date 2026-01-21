from fastapi import APIRouter, Depends, status
from app.models.base_response_model import ApiResponse
from app.models.user_models import (
    UserCreationRequest,
    UserCreationResponse,
    GetUserDetailsResponse,
)
from automapper import mapper
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User Management Service"])


from fastapi import Request, Depends, status


@router.post(
    "/create",
    response_model=ApiResponse[UserCreationResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    http_request: Request,  # ✅ FastAPI Request
    request: UserCreationRequest,  # ✅ Body
    service: UserService = Depends(UserService),
) -> ApiResponse[UserCreationResponse]:

    response = mapper.to(UserCreationResponse).map(
        service.create_user(request, http_request)
    )
    return ApiResponse(data=response)


@router.get(
    "/details/{user_id}",
    response_model=ApiResponse[GetUserDetailsResponse],
    status_code=status.HTTP_201_CREATED,
)
async def get_user_by_id(
    user_id: int, service: UserService = Depends(UserService)
) -> ApiResponse[GetUserDetailsResponse]:
    return ApiResponse(data=service.get_user_by_id(user_id))
