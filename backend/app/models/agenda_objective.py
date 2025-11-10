# app/models/agenda_objective.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class AgendaObjective(Base):
    __tablename__ = "agenda_objectives"
    objective_id = Column(Integer, primary_key=True, index=True)
    objective_name = Column(String(150), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
