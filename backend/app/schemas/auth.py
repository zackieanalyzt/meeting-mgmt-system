from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInfo(BaseModel):
    user_id: int
    username: str
    fullname: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    roles: List[str] = []
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str