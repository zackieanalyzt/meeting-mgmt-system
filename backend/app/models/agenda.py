from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.core.database import Base


class Agenda(Base):
    __tablename__ = "agendas"
    
    # ───────────────────────────────
    # Columns
    # ───────────────────────────────
    agenda_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(Integer, ForeignKey("meetings.meeting_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_local.user_id"), nullable=False)
    
    agenda_title: Mapped[str] = mapped_column(String(200), nullable=False)
    agenda_detail: Mapped[Optional[str]] = mapped_column(Text)
    agenda_type: Mapped[str] = mapped_column(String(50), default="เพื่อทราบ", nullable=False)
    agenda_order: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # ───────────────────────────────
    # Relationships
    # ───────────────────────────────
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="agendas")
    created_by: Mapped["User"] = relationship("User", back_populates="agendas")
    files: Mapped[List["File"]] = relationship(
        "File", back_populates="agenda", cascade="all, delete-orphan"
    )
    objective_maps: Mapped[List["AgendaObjectiveMap"]] = relationship(
        "AgendaObjectiveMap", 
        back_populates="agenda",
        cascade="all, delete-orphan"
    )

    # ───────────────────────────────
    # Indexes
    # ───────────────────────────────
    __table_args__ = (
        Index('idx_agenda_meeting_order', 'meeting_id', 'agenda_order'),
        Index('idx_agenda_meeting_status', 'meeting_id', 'status'),
        Index('idx_agenda_user', 'user_id'),
        Index('idx_agenda_type', 'agenda_type'),
        Index('idx_agenda_created_at', 'created_at'),
    )
