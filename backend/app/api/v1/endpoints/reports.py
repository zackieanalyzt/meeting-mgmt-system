from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def read_reports(db: Session = Depends(get_db)):
    # TODO: Get all reports
    pass

@router.get("/search")
async def search_reports(q: str, db: Session = Depends(get_db)):
    # TODO: Full-text search in reports
    pass

@router.get("/{meeting_id}")
async def read_meeting_report(meeting_id: int, db: Session = Depends(get_db)):
    # TODO: Get report by meeting
    pass