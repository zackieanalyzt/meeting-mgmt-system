from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.agenda_objective import AgendaObjective

router = APIRouter(prefix="/agenda-objectives", tags=["Agenda Objectives"])

@router.get("/")
def get_objectives(db: Session = Depends(get_db)):
    return db.query(AgendaObjective).all()

@router.post("/")
def create_objective(objective: dict, db: Session = Depends(get_db)):
    name = objective.get("objective_name")
    if not name:
        raise HTTPException(status_code=400, detail="objective_name required")
    new_obj = AgendaObjective(objective_name=name, description=objective.get("description"))
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj
