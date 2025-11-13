from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.rbac import require_admin, require_authenticated
from app.models.user import User
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingResponse, MeetingCreate, MeetingUpdate

router = APIRouter()

@router.get("/", response_model=List[MeetingResponse])
async def read_meetings(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated)
):
    """Get all meetings with pagination"""
    meetings = db.query(Meeting).order_by(Meeting.meeting_date.desc()).offset(skip).limit(limit).all()
    return meetings

@router.get("/current", response_model=MeetingResponse)
async def read_current_meeting(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated)
):
    """Get current active meeting"""
    meeting = db.query(Meeting).filter(Meeting.status == "active").order_by(Meeting.meeting_date.desc()).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="No active meeting found")
    return meeting

@router.get("/{meeting_id}", response_model=MeetingResponse)
async def read_meeting(
    meeting_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated)
):
    """Get meeting by ID"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

@router.post("/", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    meeting: MeetingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new meeting (Admin only)"""
    # db_meeting = Meeting(**meeting.model_dump())  
    # แก้ไขเพื่อให้ส่งค่า
    db_meeting = Meeting(**meeting.model_dump(),
    created_by=current_user.user_id
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: int, 
    meeting: MeetingUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update meeting (Admin only)"""
    db_meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    update_data = meeting.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meeting, field, value)
    
    db_meeting.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meeting(
    meeting_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete meeting (Admin only)"""
    db_meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    db.delete(db_meeting)
    db.commit()
    return None

@router.post("/{meeting_id}/close", response_model=MeetingResponse)
async def close_meeting(
    meeting_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Close meeting (Admin only)"""
    db_meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    db_meeting.status = "closed"
    db_meeting.closed_at = datetime.utcnow()
    db_meeting.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_meeting)
    return db_meeting