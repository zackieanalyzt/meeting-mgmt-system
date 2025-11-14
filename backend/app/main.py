from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.middleware import SecurityHeadersMiddleware, RateLimitMiddleware, sanitize_error_message
from app.api.v1.api import api_router
from app.services.auth_service import create_dummy_users

app = FastAPI(
    title="Meeting Management System",
    description="ระบบจัดการวาระและรายงานการประชุม",
    version="3.5.1"
)

# Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)

# CORS Middleware (hardened)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Specific origin only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods only
    allow_headers=["Authorization", "Content-Type"],  # Specific headers only
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to sanitize error messages
    """
    sanitized_message = sanitize_error_message(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": sanitized_message}
    )

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    from app.services.auth_service import create_dummy_users
    from app.services.objective_service import ObjectiveService
    from app.core.database import Base, postgres_engine, PostgresSessionLocal
    
    # Create all tables
    Base.metadata.create_all(bind=postgres_engine)
    print("✅ Database tables created")

    db = PostgresSessionLocal()
    try:
        create_dummy_users(db)
        print("✅ Dummy users created")
        
        # Seed default objectives
        ObjectiveService.seed_default_objectives(db)
        print("✅ Default objectives seeded")
    except Exception as e:
        print(f"❌ Startup error: {e}")
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Meeting Management System API v3.5.1", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.5.1"}