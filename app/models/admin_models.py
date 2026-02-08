from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.utils.enums import Roles


class AdminEmailRequest(BaseModel):
    subject: str
    message: str
    receiver_type: Optional[str] = None # all | admin | mentor | student
    email: Optional[EmailStr] = None
