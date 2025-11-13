from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AgendaBase(BaseModel):
    agenda_title: str
    agenda_detail: Optional[str] = None
    agenda_type: str = "เพื่อทราบ"
    agenda_order: Optional[int] = None

class AgendaCreate(BaseModel):
    agenda_title: str
    agenda_detail: Optional[str] = None
    agenda_type: str = "เพื่อทราบ"
    objective_ids: List[int] = []

class AgendaUpdate(BaseModel):
    agenda_title: Optional[str] = None
    agenda_detail: Optional[str] = None
    agenda_type: Optional[str] = None
    agenda_order: Optional[int] = None
    status: Optional[str] = None
    objective_ids: Optional[List[int]] = None

class FileInfo(BaseModel):
    file_id: int
    filename: str
    file_path: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class ObjectiveInfo(BaseModel):
    objective_id: int
    objective_name: str
    
    class Config:
        from_attributes = True

class AgendaResponse(AgendaBase):
    agenda_id: int
    meeting_id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    files: List[FileInfo] = []
    objectives: List[ObjectiveInfo] = []
    
    class Config:
        from_attributes = True