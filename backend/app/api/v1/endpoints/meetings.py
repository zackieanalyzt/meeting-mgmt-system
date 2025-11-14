from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.rbac import require_admin, require_authenticated
from app.core.audit import log_meeting_create, log_meeting_update, log_meeting_delete, log_meeting_close
from app.models.user import User
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingResponse, MeetingCreate, MeetingUpdate

router = APIRouter()

def _populate_creator_fullname(meeting: Meeting) -> dict:
    """Helper to populate created_by_fullname from creator relationship"""
    meeting_dict = {
        "meeting_id": meeting.meeting_id,
        "meeting_title": meeting.meeting_title,
        "meeting_date": meeting.meeting_date,
        "start_time": meeting.start_time,
        "end_time": meeting.end_time,
        "location": meeting.location,
        "description": meeting.description,
        "status": meeting.status,
        "created_by": meeting.created_by,
        "created_by_fullname": meeting.creator.fullname if meeting.creator else None,
        "created_at": meeting.created_at,
        "updated_at": meeting.updated_at,
        "closed_at": meeting.closed_at,
    }
    return meeting_dict

@router.get("/", response_model=List[MeetingResponse])
async def read_meetings(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated)
):
    """Get all meetings with pagination"""
    meetings = db.query(Meeting).options(joinedload(Meeting.creator)).order_by(Meeting.meeting_date.desc()).offset(skip).limit(limit).all()
    return [_populate_creator_fullname(m) for m in meetings]

@router.get("/current", response_model=MeetingResponse)
async def read_current_meeting(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated)
):
    """Get current active meeting"""
    meeting = db.query(Meeting).options(joinedload(Meeting.creator)).filter(Meeting.status == "active").order_by(Meeting.meeting_date.desc()).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="No active meeting found")
    return _populate_creator_fullname(meeting)

@router.get("/{meeting_id}", response_model=MeetingResponse)
async def read_meeting(
    meeting_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated)
):
    """Get meeting by ID"""
    meeting = db.query(Meeting).options(joinedload(Meeting.creator)).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return _populate_creator_fullname(meeting)

@router.post("/", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    meeting: MeetingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new meeting (Admin and Group Admin allowed)"""
    db_meeting = Meeting(
        **meeting.model_dump(),
        created_by=current_user.user_id
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    
    # Audit log
    log_meeting_create(current_user.username, db_meeting.meeting_id, db_meeting.meeting_title)
    
    # Reload with creator relationship
    db_meeting = db.query(Meeting).options(joinedload(Meeting.creator)).filter(Meeting.meeting_id == db_meeting.meeting_id).first()
    return _populate_creator_fullname(db_meeting)

@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: int, 
    meeting: MeetingUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update meeting (Admin and Group Admin allowed)"""
    db_meeting = db.query(Meeting).options(joinedload(Meeting.creator)).filter(Meeting.meeting_id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    update_data = meeting.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meeting, field, value)
    
    db_meeting.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_meeting)
    
    # Audit log
    log_meeting_update(current_user.username, db_meeting.meeting_id, db_meeting.meeting_title)
    
    return _populate_creator_fullname(db_meeting)

@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meeting(
    meeting_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete meeting (Admin and Group Admin allowed)"""
    db_meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Store info for audit log before deletion
    meeting_title = db_meeting.meeting_title
    
    db.delete(db_meeting)
    db.commit()
    
    # Audit log
    log_meeting_delete(current_user.username, meeting_id, meeting_title)
    
    return None

@router.post("/{meeting_id}/close", response_model=MeetingResponse)
async def close_meeting(
    meeting_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Close meeting (Admin and Group Admin allowed)"""
    db_meeting = db.query(Meeting).options(joinedload(Meeting.creator)).filter(Meeting.meeting_id == meeting_id).first()
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    db_meeting.status = "closed"
    db_meeting.closed_at = datetime.utcnow()
    db_meeting.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_meeting)
    
    # Audit log
    log_meeting_close(current_user.username, db_meeting.meeting_id, db_meeting.meeting_title)
    
    return _populate_creator_fullname(db_meeting)