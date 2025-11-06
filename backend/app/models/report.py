from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(Integer, ForeignKey("meetings.meeting_id"), nullable=False)
    report_title: Mapped[str] = mapped_column(String(200), nullable=False)
    report_summary: Mapped[Optional[str]] = mapped_column(Text)
    report_content: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users_local.user_id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="reports")
    
    # Indexes
    __table_args__ = (
        Index('idx_report_meeting', 'meeting_id'),
        Index('idx_report_status', 'status'),
        Index('idx_report_created_at', 'created_at'),
        Index('idx_report_published_at', 'published_at'),
    )