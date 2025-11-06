from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgendaBase(BaseModel):
    agenda_title: str
    agenda_detail: Optional[str] = None
    agenda_type: str = "เพื่อทราบ"
    agenda_order: Optional[int] = None

class AgendaCreate(AgendaBase):
    meeting_id: int

class AgendaUpdate(BaseModel):
    agenda_title: Optional[str] = None
    agenda_detail: Optional[str] = None
    agenda_type: Optional[str] = None
    agenda_order: Optional[int] = None
    status: Optional[str] = None

class AgendaResponse(AgendaBase):
    agenda_id: int
    meeting_id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True