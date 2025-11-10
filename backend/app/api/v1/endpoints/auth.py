from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy.orm import Session
from app.services.hr_auth_service import verify_hr_user
from app.core.auth import create_access_token
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/login")
def login(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not verify_hr_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Get user info from PostgreSQL
    user = db.query(User).filter(User.username == username).first()
    
    user_data = {
        "username": username,
        "email": user.email if user else f"{username}@hospital.local",
        "fullname": user.fullname if user else username,
        "department": user.department if user else "Unknown"
    }

    token = create_access_token(data={"sub": username})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user": user_data
    }
