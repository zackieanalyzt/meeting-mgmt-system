from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    fullname: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int
    
    class Config:
        from_attributes = True