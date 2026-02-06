from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.connectors.database_connector import get_db
from app.services.dashboard_service import DashboardService
from app.models.dashboard_models import DashboardStatsResponse
from app.models.base_response_model import ApiResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/stats",
    response_model=ApiResponse[DashboardStatsResponse],
    status_code=status.HTTP_200_OK,
    summary="Get dashboard statistics",
)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
) -> ApiResponse[DashboardStatsResponse]:
    service = DashboardService(db)
    data = await service.get_stats()
    return ApiResponse(data=data)
