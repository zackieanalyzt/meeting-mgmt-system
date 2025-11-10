# app/models/agenda_objective_map.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from app.core.database import Base

class AgendaObjectiveMap(Base):
    __tablename__ = "agenda_objective_map"
    id = Column(Integer, primary_key=True, index=True)
    agenda_id = Column(Integer, ForeignKey("agendas.agenda_id", ondelete="CASCADE"), nullable=False)
    objective_id = Column(Integer, ForeignKey("agenda_objectives.objective_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("agenda_id", "objective_id", name="uix_agenda_objective"),)
