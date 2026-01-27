from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MentorProfileRequest(BaseModel):
    user_id: int
    expertise: Optional[str] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None


class GetMentorProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    expertise: Optional[str]
    experience_years: Optional[int]
    bio: Optional[str]
    is_available: bool
    created_at: datetime
