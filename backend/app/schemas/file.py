from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileBase(BaseModel):
    file_name: str
    original_name: str
    file_type: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

class FileCreate(FileBase):
    agenda_id: int
    file_path: str

class FileResponse(FileBase):
    file_id: int
    agenda_id: int
    file_path: str
    uploaded_by: int
    uploaded_at: datetime
    is_deleted: bool
    
    class Config:
        from_attributes = True

class FileUpload(BaseModel):
    agenda_id: int