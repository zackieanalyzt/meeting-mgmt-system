from pydantic import BaseModel
from typing import Optional

class ObjectiveBase(BaseModel):
    objective_name: str

class ObjectiveCreate(ObjectiveBase):
    pass

class ObjectiveResponse(ObjectiveBase):
    objective_id: int
    
    class Config:
        from_attributes = True