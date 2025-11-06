from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportBase(BaseModel):
    report_title: str
    report_summary: Optional[str] = None
    report_content: Optional[str] = None

class ReportCreate(ReportBase):
    meeting_id: int

class ReportUpdate(BaseModel):
    report_title: Optional[str] = None
    report_summary: Optional[str] = None
    report_content: Optional[str] = None
    status: Optional[str] = None

class ReportResponse(ReportBase):
    report_id: int
    meeting_id: int
    status: str
    file_path: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True