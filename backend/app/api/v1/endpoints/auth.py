from fastapi import APIRouter, HTTPException, Form, Depends, Request
from sqlalchemy.orm import Session
from app.services.hr_auth_service import verify_hr_user
from app.core.auth import create_access_token, get_user_roles
from app.core.database import get_db
from app.core.audit import log_login_success, log_login_failure
from app.models.user import User

router = APIRouter()

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    
    if not verify_hr_user(username, password):
        log_login_failure(username, client_ip)
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Get user info from PostgreSQL
    user = db.query(User).filter(User.username == username).first()
    
    # Get user roles
    roles = []
    if user:
        roles = get_user_roles(user, db)
    
    user_data = {
        "username": username,
        "email": user.email if user else f"{username}@hospital.local",
        "fullname": user.fullname if user else username,
        "department": user.department if user else "Unknown",
        "roles": roles
    }

    token = create_access_token(data={"sub": username})
    
    # Log successful login
    log_login_success(username, client_ip)
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user": user_data
    }
