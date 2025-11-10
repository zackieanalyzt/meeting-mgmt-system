from fastapi import APIRouter, HTTPException, Form
from app.services.hr_auth_service import verify_hr_user
from app.core.auth import create_access_token

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if not verify_hr_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(data={"sub": username})
    return {"access_token": token, "token_type": "bearer"}
