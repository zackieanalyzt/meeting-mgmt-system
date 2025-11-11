from sqlalchemy.orm import Session
from datetime import datetime
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate, MeetingUpdate

class MeetingService:
    @staticmethod
    def create_meeting(db: Session, meeting_data: MeetingCreate, user_id: int) -> Meeting:
        """Create a new meeting"""
        meeting = Meeting(
            meeting_title=meeting_data.meeting_title,
            meeting_date=meeting_data.meeting_date,
            start_time=meeting_data.start_time,
            end_time=meeting_data.end_time,
            location=meeting_data.location,
            description=meeting_data.description,
            created_by=user_id,
            status="active"
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        return meeting
    
    @staticmethod
    def get_meeting(db: Session, meeting_id: int) -> Meeting:
        """Get meeting by ID"""
        return db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    
    @staticmethod
    def get_meetings(db: Session, skip: int = 0, limit: int = 100) -> list[Meeting]:
        """Get all meetings with pagination"""
        return db.query(Meeting).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_meeting(db: Session, meeting_id: int, meeting_data: MeetingUpdate) -> Meeting:
        """Update meeting"""
        meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            return None
        
        update_data = meeting_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(meeting, field, value)
        
        db.commit()
        db.refresh(meeting)
        return meeting
    
    @staticmethod
    def delete_meeting(db: Session, meeting_id: int) -> bool:
        """Delete meeting"""
        meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            return False
        
        db.delete(meeting)
        db.commit()
        return True
    
    @staticmethod
    def close_meeting(db: Session, meeting_id: int) -> Meeting:
        """Close meeting"""
        meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            return None
        
        meeting.status = "closed"
        meeting.closed_at = datetime.utcnow()
        db.commit()
        db.refresh(meeting)
        return meeting