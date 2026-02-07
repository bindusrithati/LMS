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

        # 4. Student Enrollment Trend (Group by Month)
        from sqlalchemy import extract
        import calendar
        from datetime import datetime

        current_year = datetime.now().year
        
        # Initialize dictionary with 0 for all months
        monthly_counts = {calendar.month_abbr[i]: 0 for i in range(1, 13)}

        enrollment_data = (
            self.db.query(
                func.extract('month', User.created_at).label('month'),
                func.count(User.id).label('count')
            )
            .filter(
                User._User__role == Roles.Student.value,
                User.is_active == True,
                func.extract('year', User.created_at) == current_year
            )
            .group_by(func.extract('month', User.created_at))
            .all()
        )

        for month_num, count in enrollment_data:
            month_name = calendar.month_abbr[int(month_num)]
            monthly_counts[month_name] = count

        # Convert to list of EnrollmentTrend objects
        from app.models.dashboard_models import EnrollmentTrend
        
        # Only show up to current month or all months? 
        # Requirement says "Trend", usually means past data. 
        # Let's show all months for this year as per typical dashboard requirements.
        # Ensure correct order Jan -> Dec
        enrollment_trend = [
            EnrollmentTrend(month=m, students=monthly_counts[m]) 
            for m in list(calendar.month_abbr)[1:]
        ]

        return DashboardStatsResponse(
            total_users=total_users,
            total_students=total_students,
            total_mentors=total_mentors,
            total_admins=total_admins,
            active_batches=active_batches,
            total_batches=total_batches,
            role_distribution=role_distribution,
            enrollment_trend=enrollment_trend,
        )
