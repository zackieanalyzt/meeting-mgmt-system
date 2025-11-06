from pydantic import BaseModel
from typing import Optional

class AgendaBase(BaseModel):
    agenda_title: str
    agenda_detail: Optional[str] = None
    agenda_type: Optional[str] = "เพื่อทราบ"

class AgendaCreate(AgendaBase):
    meeting_id: int

class AgendaResponse(AgendaBase):
    agenda_id: int
    meeting_id: int
    user_id: int
    
    class Config:
        from_attributes = True