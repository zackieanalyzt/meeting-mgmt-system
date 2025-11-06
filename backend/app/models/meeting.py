from sqlalchemy import String, Integer, Date, DateTime, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import List, Optional
from app.core.database import Base

class Meeting(Base):
    __tablename__ = "meetings"
    
    meeting_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_name: Mapped[str] = mapped_column(String(200), nullable=False)
    meeting_date: Mapped[date] = mapped_column(Date, nullable=False)
    meeting_time: Mapped[Optional[str]] = mapped_column(String(20))
    location: Mapped[Optional[str]] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    agendas: Mapped[List["Agenda"]] = relationship("Agenda", back_populates="meeting", cascade="all, delete-orphan")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="meeting", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_meeting_date_status', 'meeting_date', 'status'),
        Index('idx_meeting_status', 'status'),
        Index('idx_meeting_created_at', 'created_at'),
    )