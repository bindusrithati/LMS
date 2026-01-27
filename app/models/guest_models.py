from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GuestRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    purpose: str  # demo | enquiry | trial


class GetGuestResponse(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    purpose: str
    created_at: datetime
