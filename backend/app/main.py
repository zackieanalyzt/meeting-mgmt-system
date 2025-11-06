from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.api.v1.api import api_router
from app.services.auth_service import create_dummy_users

app = FastAPI(
    title="Meeting Management System",
    description="ระบบจัดการวาระและรายงานการประชุม",
    version="3.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize dummy data on startup"""
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        create_dummy_users(db)
        print("✅ Dummy users created successfully")
    except Exception as e:
        print(f"❌ Error creating dummy users: {e}")
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Meeting Management System API v3.3", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.3.0"}