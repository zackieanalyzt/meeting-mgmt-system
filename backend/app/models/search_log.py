from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class SearchLog(Base):
    __tablename__ = "search_log"
    
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    search_text = Column(String(500))
    search_target = Column(String(100))
    search_time = Column(DateTime)