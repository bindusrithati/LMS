from datetime import datetime
import sqlalchemy as sa
from app.connectors.database_connector import Base


class Guest(Base):
    __tablename__ = "guests"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name: str = sa.Column(sa.String(50), nullable=True)
    email: str = sa.Column(sa.String(100), nullable=True)
    phone_number: str = sa.Column(sa.String(20), nullable=True)
    purpose: str = sa.Column(sa.String(50), nullable=False)
    # demo | enquiry | trial
    created_at: datetime = sa.Column(sa.DateTime, default=sa.func.now(), nullable=False)
