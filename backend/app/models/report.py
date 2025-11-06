from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    report_id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.meeting_id"))
    report_title = Column(String(200))
    report_summary = Column(Text)
    file_path = Column(String(500))