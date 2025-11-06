from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Agenda(Base):
    __tablename__ = "agendas"
    
    agenda_id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.meeting_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    agenda_title = Column(String(200))
    agenda_detail = Column(Text)
    agenda_type = Column(String(50))