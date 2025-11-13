from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile
import os
import uuid
from datetime import datetime
from app.models.agenda import Agenda
from app.models.file import File
from app.models.objective import AgendaObjectiveMap
from app.schemas.agenda import AgendaCreate, AgendaUpdate

class AgendaService:
    UPLOAD_DIR = "uploads"
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.md', '.jpg', '.jpeg', '.png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_FILES = 10
    
    @staticmethod
    def create_agenda(
        db: Session, 
        meeting_id: int,
        agenda_data: AgendaCreate, 
        user_id: int,
        files: List[UploadFile] = None
    ) -> Agenda:
        """Create a new agenda with optional file uploads"""
        
        # Create agenda
        agenda = Agenda(
            meeting_id=meeting_id,
            user_id=user_id,
            agenda_title=agenda_data.agenda_title,
            agenda_detail=agenda_data.agenda_detail,
            agenda_type=agenda_data.agenda_type,
            status="pending"
        )
        db.add(agenda)
        db.flush()  # Get agenda_id
        
        # Link objectives
        if agenda_data.objective_ids:
            for objective_id in agenda_data.objective_ids:
                obj_map = AgendaObjectiveMap(
                    agenda_id=agenda.agenda_id,
                    objective_id=objective_id
                )
                db.add(obj_map)
        
        # Handle file uploads
        if files:
            AgendaService._save_files(db, agenda.agenda_id, files, user_id)
        
        db.commit()
        db.refresh(agenda)
        return agenda
    
    @staticmethod
    def _save_files(db: Session, agenda_id: int, files: List[UploadFile], user_id: int):
        """Save uploaded files"""
        if len(files) > AgendaService.MAX_FILES:
            raise ValueError(f"Maximum {AgendaService.MAX_FILES} files allowed")
        
        # Create upload directory if not exists
        os.makedirs(AgendaService.UPLOAD_DIR, exist_ok=True)
        
        for upload_file in files:
            # Validate file extension
            file_ext = os.path.splitext(upload_file.filename)[1].lower()
            if file_ext not in AgendaService.ALLOWED_EXTENSIONS:
                raise ValueError(f"File type {file_ext} not allowed")
            
            # Validate file size
            upload_file.file.seek(0, 2)  # Seek to end
            file_size = upload_file.file.tell()
            upload_file.file.seek(0)  # Reset to beginning
            
            if file_size > AgendaService.MAX_FILE_SIZE:
                raise ValueError(f"File {upload_file.filename} exceeds 10 MB limit")
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(AgendaService.UPLOAD_DIR, unique_filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(upload_file.file.read())
            
            # Create file record
            file_record = File(
                agenda_id=agenda_id,
                file_name=unique_filename,
                original_name=upload_file.filename,
                file_path=file_path,
                file_type=file_ext,
                file_size=file_size,
                mime_type=upload_file.content_type,
                uploaded_by=user_id
            )
            db.add(file_record)
    
    @staticmethod
    def get_agenda(db: Session, agenda_id: int) -> Agenda:
        """Get agenda by ID with files and objectives"""
        return db.query(Agenda).filter(Agenda.agenda_id == agenda_id).first()
    
    @staticmethod
    def get_meeting_agendas(db: Session, meeting_id: int) -> List[Agenda]:
        """Get all agendas for a meeting"""
        return db.query(Agenda).filter(Agenda.meeting_id == meeting_id).all()
    
    @staticmethod
    def update_agenda(
        db: Session, 
        agenda_id: int, 
        agenda_data: AgendaUpdate,
        files: List[UploadFile] = None
    ) -> Agenda:
        """Update agenda"""
        agenda = db.query(Agenda).filter(Agenda.agenda_id == agenda_id).first()
        if not agenda:
            return None
        
        # Update basic fields
        update_data = agenda_data.model_dump(exclude_unset=True, exclude={'objective_ids'})
        for field, value in update_data.items():
            setattr(agenda, field, value)
        
        # Update objectives if provided
        if agenda_data.objective_ids is not None:
            # Remove old mappings
            db.query(AgendaObjectiveMap).filter(
                AgendaObjectiveMap.agenda_id == agenda_id
            ).delete()
            
            # Add new mappings
            for objective_id in agenda_data.objective_ids:
                obj_map = AgendaObjectiveMap(
                    agenda_id=agenda_id,
                    objective_id=objective_id
                )
                db.add(obj_map)
        
        # Add new files if provided
        if files:
            AgendaService._save_files(db, agenda_id, files, agenda.user_id)
        
        db.commit()
        db.refresh(agenda)
        return agenda
    
    @staticmethod
    def delete_agenda(db: Session, agenda_id: int) -> bool:
        """Delete agenda"""
        agenda = db.query(Agenda).filter(Agenda.agenda_id == agenda_id).first()
        if not agenda:
            return False
        
        db.delete(agenda)
        db.commit()
        return True