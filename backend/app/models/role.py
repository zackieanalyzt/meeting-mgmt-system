from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True)

class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(DateTime)