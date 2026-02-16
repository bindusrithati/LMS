from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str
    password: str
    role: str
    phone_number: str


class UserUpdateRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str
    role: str
    phone_number: str
    is_active: bool


class UserCreationResponse(BaseModel):
    id: int
    message: str


class GetUserDetailsResponse(BaseModel):
    id: int
    name: str
    email: str
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    role: str
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: datetime
    updated_by: Optional[str] = None
    is_active: bool


class CurrentContextUser:
    id: int
    name: str
    email: str
    role: str


class UserInfoResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
