from pydantic import BaseModel, field_validator
from datetime import date, datetime, time
from typing import Optional

class MeetingBase(BaseModel):
    meeting_title: str
    meeting_date: date
    start_time: time
    end_time: time
    location: str
    description: Optional[str] = None

class MeetingCreate(MeetingBase):
    @field_validator('end_time')
    @classmethod
    def validate_times(cls, v, info):
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class MeetingUpdate(BaseModel):
    meeting_title: Optional[str] = None
    meeting_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class MeetingResponse(MeetingBase):
    meeting_id: int
    status: str
    created_by: int
    created_by_fullname: Optional[str] = None  # Added for Priority 3
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True