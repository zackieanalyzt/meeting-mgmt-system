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
def startup_event():
    from app.services.auth_service import create_dummy_users
    from app.core.database import Base, postgres_engine, PostgresSessionLocal  # ✅ เพิ่ม Base, engine
    Base.metadata.create_all(bind=postgres_engine)  # ✅ ให้ SQLAlchemy สร้างตารางทั้งหมด

    db = PostgresSessionLocal()
    create_dummy_users(db)
    db.close()


@app.get("/")
async def root():
    return {"message": "Meeting Management System API v3.3", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.3.0"}