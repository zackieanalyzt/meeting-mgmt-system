from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.agenda import AgendaResponse, AgendaCreate

router = APIRouter()

@router.get("/", response_model=list[AgendaResponse])
async def read_agendas(meeting_id: int = None, db: Session = Depends(get_db)):
    # TODO: Get agendas by meeting
    pass

@router.post("/", response_model=AgendaResponse)
async def create_agenda(agenda: AgendaCreate, db: Session = Depends(get_db)):
    # TODO: Create new agenda
    pass

@router.put("/{agenda_id}", response_model=AgendaResponse)
async def update_agenda(agenda_id: int, agenda: AgendaCreate, db: Session = Depends(get_db)):
    # TODO: Update agenda
    pass

@router.delete("/{agenda_id}")
async def delete_agenda(agenda_id: int, db: Session = Depends(get_db)):
    # TODO: Delete agenda
    pass