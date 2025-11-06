from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.file import FileResponse as FileResponseSchema, FileUpload

router = APIRouter()

@router.get("/", response_model=List[FileResponseSchema])
async def read_files(
    agenda_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get files, optionally filtered by agenda"""
    # TODO: Get files by agenda
    pass

@router.get("/{file_id}", response_model=FileResponseSchema)
async def read_file(file_id: int, db: Session = Depends(get_db)):
    """Get file metadata by ID"""
    # TODO: Get file metadata
    pass

@router.get("/{file_id}/download")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    """Download file by ID"""
    # TODO: Handle file download
    pass

@router.post("/upload", response_model=FileResponseSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    agenda_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload file to agenda"""
    # TODO: Handle file upload
    pass

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    """Delete file (soft delete)"""
    # TODO: Delete file
    pass