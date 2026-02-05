from pydantic import BaseModel, EmailStr, Field

from app.utils.enums import Roles


class AdminEmailRequest(BaseModel):
    email: EmailStr
    receiver_type: Roles
