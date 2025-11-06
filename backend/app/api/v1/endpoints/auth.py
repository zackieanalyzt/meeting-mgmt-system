from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import create_access_token, get_current_active_user, get_user_roles
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import Token, UserInfo
from app.schemas.user import UserResponse

router = APIRouter()

def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Authenticate user with dummy data from users_local table
    TODO: Implement actual MD5 hash verification with MariaDB
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    # For now, accept any password for demo purposes
    # TODO: Implement MD5 hash verification against MariaDB
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.user_id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout():
    """
    Logout endpoint - client should remove token
    TODO: Implement token blacklisting if needed
    """
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserInfo)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user information with roles"""
    user_roles = get_user_roles(current_user, db)
    
    return UserInfo(
        user_id=current_user.user_id,
        username=current_user.username,
        fullname=current_user.fullname,
        department=current_user.department,
        email=current_user.email,
        roles=user_roles
    )

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_active_user)):
    """Verify if token is valid"""
    return {"valid": True, "username": current_user.username}