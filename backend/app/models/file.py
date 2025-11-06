from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class File(Base):
    __tablename__ = "files"
    
    file_id = Column(Integer, primary_key=True, index=True)
    agenda_id = Column(Integer, ForeignKey("agendas.agenda_id"))
    file_name = Column(String(255))
    file_path = Column(String(500))
    file_type = Column(String(20))
    uploaded_by = Column(Integer, ForeignKey("users.user_id"))