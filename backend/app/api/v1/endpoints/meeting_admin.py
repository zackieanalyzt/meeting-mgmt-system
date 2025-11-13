from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.rbac import require_any_admin
from app.models.user import User
from app.schemas.meeting import MeetingResponse, MeetingCreate
from app.schemas.agenda import AgendaResponse, AgendaCreate
from app.schemas.objective import ObjectiveResponse, ObjectiveCreate
from app.services.meeting_service import MeetingService
from app.services.agenda_service import AgendaService
from app.services.objective_service import ObjectiveService
import json

router = APIRouter()

# ==================== MEETING ENDPOINTS ====================

@router.post("/meetings", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    meeting: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """
    Create a new meeting (Group Admin or Main Admin)
    
    Validates:
    - start_time < end_time
    - All required fields present
    """
    try:
        new_meeting = MeetingService.create_meeting(db, meeting, current_user.user_id)
        return new_meeting
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/meetings", response_model=List[MeetingResponse])
async def get_meetings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """Get all meetings with pagination"""
    meetings = MeetingService.get_meetings(db, skip, limit)
    return meetings

@router.get("/meetings/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """Get meeting by ID"""
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

# ==================== AGENDA ENDPOINTS ====================

@router.post("/meetings/{meeting_id}/agendas", response_model=AgendaResponse, status_code=status.HTTP_201_CREATED)
async def create_agenda(
    meeting_id: int,
    agenda_title: str = Form(...),
    agenda_detail: Optional[str] = Form(None),
    agenda_type: str = Form("เพื่อทราบ"),
    objective_ids: str = Form("[]"),  # JSON string of list
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """
    Create agenda with file uploads
    
    Supports:
    - Up to 10 files
    - Max 10 MB per file
    - Allowed types: pdf, doc, docx, md, jpg, jpeg, png
    """
    # Verify meeting exists
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Parse objective_ids
    try:
        objective_ids_list = json.loads(objective_ids)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid objective_ids format")
    
    # Create agenda data
    agenda_data = AgendaCreate(
        agenda_title=agenda_title,
        agenda_detail=agenda_detail,
        agenda_type=agenda_type,
        objective_ids=objective_ids_list
    )
    
    try:
        new_agenda = AgendaService.create_agenda(
            db, meeting_id, agenda_data, current_user.user_id, files
        )
        
        # Refresh to load relationships
        db.refresh(new_agenda)
        
        # Build response with files and objectives
        response = AgendaResponse(
            agenda_id=new_agenda.agenda_id,
            meeting_id=new_agenda.meeting_id,
            user_id=new_agenda.user_id,
            agenda_title=new_agenda.agenda_title,
            agenda_detail=new_agenda.agenda_detail,
            agenda_type=new_agenda.agenda_type,
            agenda_order=new_agenda.agenda_order,
            status=new_agenda.status,
            created_at=new_agenda.created_at,
            updated_at=new_agenda.updated_at,
            files=[{
                "file_id": f.file_id,
                "filename": f.original_name,
                "file_path": f.file_path,
                "uploaded_at": f.uploaded_at
            } for f in new_agenda.files],
            objectives=[{
                "objective_id": om.objective.objective_id,
                "objective_name": om.objective.objective_name
            } for om in new_agenda.objective_maps]
        )
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/meetings/{meeting_id}/agendas", response_model=List[AgendaResponse])
async def get_meeting_agendas(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """Get all agendas for a meeting with files and objectives"""
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    agendas = AgendaService.get_meeting_agendas(db, meeting_id)
    
    # Build response with relationships
    response = []
    for agenda in agendas:
        response.append(AgendaResponse(
            agenda_id=agenda.agenda_id,
            meeting_id=agenda.meeting_id,
            user_id=agenda.user_id,
            agenda_title=agenda.agenda_title,
            agenda_detail=agenda.agenda_detail,
            agenda_type=agenda.agenda_type,
            agenda_order=agenda.agenda_order,
            status=agenda.status,
            created_at=agenda.created_at,
            updated_at=agenda.updated_at,
            files=[{
                "file_id": f.file_id,
                "filename": f.original_name,
                "file_path": f.file_path,
                "uploaded_at": f.uploaded_at
            } for f in agenda.files],
            objectives=[{
                "objective_id": om.objective.objective_id,
                "objective_name": om.objective.objective_name
            } for om in agenda.objective_maps]
        ))
    
    return response

# ==================== OBJECTIVE ENDPOINTS ====================

@router.get("/objectives", response_model=List[ObjectiveResponse])
async def get_objectives(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """Get all objectives"""
    objectives = ObjectiveService.get_objectives(db)
    return objectives

@router.post("/objectives", response_model=ObjectiveResponse, status_code=status.HTTP_201_CREATED)
async def create_objective(
    objective: ObjectiveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_admin)
):
    """Create new objective (Admin only)"""
    try:
        new_objective = ObjectiveService.create_objective(db, objective)
        return new_objective
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))