from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.post("/upload")
async def upload_file(
    agenda_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # TODO: Handle file upload
    pass

@router.get("/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    # TODO: Handle file download
    pass

@router.delete("/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    # TODO: Delete file
    pass