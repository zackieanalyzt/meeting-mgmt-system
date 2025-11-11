from sqlalchemy import String, Integer, Date, DateTime, Text, Time, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date, time
from typing import List, Optional
from app.core.database import Base

class Meeting(Base):
    __tablename__ = "meetings"
    
    meeting_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_title: Mapped[str] = mapped_column(String(200), nullable=False)
    meeting_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users_local.user_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    agendas: Mapped[List["Agenda"]] = relationship("Agenda", back_populates="meeting", cascade="all, delete-orphan")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="meeting", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_meeting_date_status', 'meeting_date', 'status'),
        Index('idx_meeting_status', 'status'),
        Index('idx_meeting_created_at', 'created_at'),
        Index('idx_meeting_created_by', 'created_by'),
    )