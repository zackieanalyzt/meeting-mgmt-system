from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.core.database import Base

class AgendaObjective(Base):
    __tablename__ = "agenda_objective"
    
    objective_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    objective_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Relationships
    agenda_maps: Mapped[List["AgendaObjectiveMap"]] = relationship(
        "AgendaObjectiveMap", 
        back_populates="objective",
        cascade="all, delete-orphan"
    )

class AgendaObjectiveMap(Base):
    __tablename__ = "agenda_objective_map"
    
    agenda_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("agendas.agenda_id", ondelete="CASCADE"), 
        primary_key=True
    )
    objective_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("agenda_objective.objective_id", ondelete="CASCADE"), 
        primary_key=True
    )
    
    # Relationships
    agenda: Mapped["Agenda"] = relationship("Agenda", back_populates="objective_maps")
    objective: Mapped["AgendaObjective"] = relationship("AgendaObjective", back_populates="agenda_maps")