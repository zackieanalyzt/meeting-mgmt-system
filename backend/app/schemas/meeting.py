from pydantic import BaseModel
from datetime import date
from typing import Optional

class MeetingBase(BaseModel):
    meeting_name: str
    meeting_date: date
    meeting_time: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = "active"

class MeetingCreate(MeetingBase):
    pass

class MeetingResponse(MeetingBase):
    meeting_id: int
    
    class Config:
        from_attributes = True