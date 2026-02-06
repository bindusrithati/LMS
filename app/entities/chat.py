from datetime import datetime
import sqlalchemy as sa
from app.connectors.database_connector import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    batch_id: int = sa.Column(sa.Integer, sa.ForeignKey("batches.id"), nullable=False)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    message: str = sa.Column(sa.String, nullable=False)
    timestamp: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
