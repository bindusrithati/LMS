from sqlalchemy.orm import Session
from sqlalchemy import func
from app.entities.user import User
from app.entities.batch import Batch
from app.utils.enums import Roles
from app.models.dashboard_models import DashboardStatsResponse, RoleDistribution


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    async def get_stats(self) -> DashboardStatsResponse:
        # 1. User Counts
        total_users = (
            self.db.query(func.count(User.id)).filter(User.is_active == True).scalar()
            or 0
        )
        total_students = (
            self.db.query(func.count(User.id))
            .filter(User._User__role == Roles.Student.value, User.is_active == True)
            .scalar()
            or 0
        )
        total_mentors = (
            self.db.query(func.count(User.id))
            .filter(User._User__role == Roles.Mentor.value, User.is_active == True)
            .scalar()
            or 0
        )
        total_admins = (
            self.db.query(func.count(User.id))
            .filter(User._User__role == Roles.Admin.value, User.is_active == True)
            .scalar()
            or 0
        )

        # 2. Batch Counts
        total_batches = self.db.query(func.count(Batch.id)).scalar() or 0
        active_batches = (
            self.db.query(func.count(Batch.id)).filter(Batch.is_active == True).scalar()
            or 0
        )

        # 3. Role Distribution for Pie Chart
        role_distribution = [
            RoleDistribution(name="Students", value=total_students, color="#667eea"),
            RoleDistribution(name="Mentors", value=total_mentors, color="#764ba2"),
            RoleDistribution(name="Admins", value=total_admins, color="#1976d2"),
        ]

        return DashboardStatsResponse(
            total_users=total_users,
            total_students=total_students,
            total_mentors=total_mentors,
            total_admins=total_admins,
            active_batches=active_batches,
            total_batches=total_batches,
            role_distribution=role_distribution,
        )
