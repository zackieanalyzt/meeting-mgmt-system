from sqlalchemy import String, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.core.database import Base

class SearchLog(Base):
    __tablename__ = "search_log"
    
    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_local.user_id"), nullable=False)
    search_text: Mapped[str] = mapped_column(String(500), nullable=False)
    search_target: Mapped[str] = mapped_column(String(100), nullable=False)
    search_results_count: Mapped[Optional[int]] = mapped_column(Integer)
    search_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="search_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_search_log_user', 'user_id'),
        Index('idx_search_log_time', 'search_time'),
        Index('idx_search_log_target', 'search_target'),
        Index('idx_search_log_user_time', 'user_id', 'search_time'),
    )