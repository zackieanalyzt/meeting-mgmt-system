from functools import wraps
from typing import List, Union
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_active_user, get_user_roles
from app.core.database import get_db
from app.models.user import User

class RoleChecker:
    def __init__(self, allowed_roles: Union[str, List[str]]):
        if isinstance(allowed_roles, str):
            allowed_roles = [allowed_roles]
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
        user_roles = get_user_roles(user, db)
        
        if not any(role in user_roles for role in self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of these roles: {', '.join(self.allowed_roles)}"
            )
        return user

# Role-based decorators
def require_roles(roles: Union[str, List[str]]):
    """Decorator to require specific roles"""
    return RoleChecker(roles)

# Predefined role checkers based on the system specification
require_admin = RoleChecker(["Admin ใหญ่"])
require_group_admin = RoleChecker(["Admin กลุ่มงาน", "Admin ใหญ่"])
require_any_admin = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน"])
require_authenticated = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน", "ผู้ใช้ทั่วไป"])

# Permission matrix based on the specification
class Permissions:
    @staticmethod
    def can_create_meeting(user_roles: List[str]) -> bool:
        return "Admin ใหญ่" in user_roles
    
    @staticmethod
    def can_approve_agenda(user_roles: List[str]) -> bool:
        return "Admin ใหญ่" in user_roles
    
    @staticmethod
    def can_add_agenda(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in ["Admin ใหญ่", "Admin กลุ่มงาน"])
    
    @staticmethod
    def can_upload_file(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in ["Admin ใหญ่", "Admin กลุ่มงาน"])
    
    @staticmethod
    def can_edit_before_close(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in ["Admin ใหญ่", "Admin กลุ่มงาน"])
    
    @staticmethod
    def can_close_meeting(user_roles: List[str]) -> bool:
        return "Admin ใหญ่" in user_roles
    
    @staticmethod
    def can_manage_reports(user_roles: List[str]) -> bool:
        return "Admin ใหญ่" in user_roles
    
    @staticmethod
    def can_search_reports(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in ["Admin ใหญ่", "Admin กลุ่มงาน", "ผู้ใช้ทั่วไป"])
    
    @staticmethod
    def can_view_agenda(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in ["Admin ใหญ่", "Admin กลุ่มงาน", "ผู้ใช้ทั่วไป"])