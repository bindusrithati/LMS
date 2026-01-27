from datetime import datetime
import sqlalchemy as sa
from app.connectors.database_connector import Base
from sqlalchemy.orm import relationship


class MentorProfile(Base):
    __tablename__ = "mentor_profiles"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    user_id: int = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    expertise: str = sa.Column(sa.String(100), nullable=True)
    experience_years: int = sa.Column(sa.Integer, nullable=True)
    bio: str = sa.Column(sa.String(500), nullable=True)
    is_available: bool = sa.Column(sa.Boolean, default=True, nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, default=sa.func.now(), nullable=False)
    updated_at: datetime = sa.Column(
        sa.DateTime,
        default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
    user = relationship("User", back_populates="mentor_profile")
