from sqlalchemy import String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_roles: Mapped[List["UserRole"]] = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_local.user_id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    assigned_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users_local.user_id"))
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="user_roles", foreign_keys=[user_id])
    role: Mapped["Role"] = relationship("Role", back_populates="user_roles")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_role_composite', 'user_id', 'role_id'),
        Index('idx_user_role_assigned_at', 'assigned_at'),
    )