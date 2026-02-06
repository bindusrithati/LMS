from datetime import date, datetime, time
from typing import Optional, List

from pydantic import BaseModel

from app.utils.enums import Days


class BatchRequest(BaseModel):
    name: Optional[str] = None
    syllabus_ids: Optional[List[int]] = None
    start_date: date
    end_date: date
    mentor: int
    is_active: Optional[bool] = True


class GetBatchResponse(BaseModel):
    id: int
    name: Optional[str] = None
    syllabus: List[dict] = None
    start_date: date
    end_date: date
    mentor: Optional[int]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    is_active: bool


class ClassScheduleRequest(BaseModel):
    day: Days
    start_time: time
    end_time: time
    topic: Optional[str] = None


class GetClassScheduleResponse(BaseModel):
    id: int
    day: int
    start_time: time
    end_time: time
    topic: Optional[str] = None
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    is_active: bool


class UpdateClassScheduleRequest(BaseModel):
    day: Days
    start_time: time
    end_time: time
    topic: Optional[str] = None
