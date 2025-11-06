from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class MeetingBase(BaseModel):
    meeting_name: str
    meeting_date: date
    meeting_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None

class MeetingCreate(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    meeting_name: Optional[str] = None
    meeting_date: Optional[date] = None
    meeting_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class MeetingResponse(MeetingBase):
    meeting_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True