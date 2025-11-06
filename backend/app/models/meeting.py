from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class Meeting(Base):
    __tablename__ = "meetings"
    
    meeting_id = Column(Integer, primary_key=True, index=True)
    meeting_name = Column(String(200))
    meeting_date = Column(Date)
    meeting_time = Column(String(20))
    location = Column(String(200))
    status = Column(String(20))