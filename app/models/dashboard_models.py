from typing import List, Optional
from pydantic import BaseModel

class RoleDistribution(BaseModel):
    name: str
    value: int
    color: str


class EnrollmentTrend(BaseModel):
    month: str
    students: int

class DashboardStatsResponse(BaseModel):
    total_users: int
    total_students: int
    total_mentors: int
    total_admins: int
    active_batches: int
    total_batches: int
    role_distribution: List[RoleDistribution]
    enrollment_trend: List[EnrollmentTrend]
