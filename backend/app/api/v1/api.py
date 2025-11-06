from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, meetings, agendas, files, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(agendas.router, prefix="/agendas", tags=["agendas"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])