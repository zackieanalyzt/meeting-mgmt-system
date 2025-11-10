# app/models/__init__.py
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.meeting import Meeting
from app.models.agenda import Agenda
from app.models.file import File
from app.models.report import Report
from app.models.agenda_objective import AgendaObjective
from app.models.agenda_objective_map import AgendaObjectiveMap  # ✅ เพิ่มบรรทัดนี้
from .search_log import SearchLog

# Import all models to ensure they are registered with SQLAlchemy
__all__ = [
    "User",
    "Role",
    "UserRole",
    "Meeting",
    "Agenda",
    "File",
    "Report",
    "SearchLog"
]
