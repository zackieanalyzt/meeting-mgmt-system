from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.meeting import MeetingResponse, MeetingCreate

router = APIRouter()

@router.get("/", response_model=list[MeetingResponse])
async def read_meetings(db: Session = Depends(get_db)):
    # TODO: Get all meetings
    pass

@router.get("/current", response_model=MeetingResponse)
async def read_current_meeting(db: Session = Depends(get_db)):
    # TODO: Get current meeting
    pass

@router.post("/", response_model=MeetingResponse)
async def create_meeting(meeting: MeetingCreate, db: Session = Depends(get_db)):
    # TODO: Create new meeting
    pass