from sqlalchemy import String, Integer, ForeignKey, DateTime, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.core.database import Base

class File(Base):
    __tablename__ = "files"
    
    file_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agenda_id: Mapped[int] = mapped_column(Integer, ForeignKey("agendas.agenda_id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    uploaded_by: Mapped[int] = mapped_column(Integer, ForeignKey("users_local.user_id"), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    agenda: Mapped["Agenda"] = relationship("Agenda", back_populates="files")
    uploader: Mapped["User"] = relationship("User", back_populates="uploaded_files")
    
    # Indexes
    __table_args__ = (
        Index('idx_file_agenda', 'agenda_id'),
        Index('idx_file_uploader', 'uploaded_by'),
        Index('idx_file_type', 'file_type'),
        Index('idx_file_uploaded_at', 'uploaded_at'),
        Index('idx_file_deleted', 'is_deleted'),
    )