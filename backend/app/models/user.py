from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.core.database import Base

class User(Base):
    __tablename__ = "users_local"
    
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String(100))
    department: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    
    # ✅ Relationships (ระบุ foreign_keys ชัดเจน)
    user_roles: Mapped[List["UserRole"]] = relationship(
        "UserRole",
        back_populates="user",
        foreign_keys="[UserRole.user_id]"
    )
    
    agendas: Mapped[List["Agenda"]] = relationship(
        "Agenda",
        back_populates="created_by"
    )
    
    uploaded_files: Mapped[List["File"]] = relationship(
        "File",
        back_populates="uploader"
    )
    
    search_logs: Mapped[List["SearchLog"]] = relationship(
        "SearchLog",
        back_populates="user"
    )
