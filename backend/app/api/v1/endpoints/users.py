from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(db: Session = Depends(get_db)):
    # TODO: Get current user
    pass

@router.get("/", response_model=list[UserResponse])
async def read_users(db: Session = Depends(get_db)):
    # TODO: Get all users
    pass