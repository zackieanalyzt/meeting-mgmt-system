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
# Support both Thai and English role names for flexibility
# UPDATED: require_admin now allows both admin_main and admin_group to create meetings
require_admin = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน", "admin_main", "admin_group"])
require_group_admin = RoleChecker(["Admin กลุ่มงาน", "Admin ใหญ่", "admin_group", "admin_main"])
require_any_admin = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน", "admin_main", "admin_group"])
require_authenticated = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน", "ผู้ใช้ทั่วไป", "admin_main", "admin_group", "user"])

# Permission matrix based on the specification
class Permissions:
    # Admin role names (support both Thai and English)
    ADMIN_MAIN = ["Admin ใหญ่", "admin_main"]
    ADMIN_GROUP = ["Admin กลุ่มงาน", "admin_group"]
    USER_GENERAL = ["ผู้ใช้ทั่วไป", "user"]
    ANY_ADMIN = ADMIN_MAIN + ADMIN_GROUP
    ALL_ROLES = ADMIN_MAIN + ADMIN_GROUP + USER_GENERAL
    
    @staticmethod
    def can_create_meeting(user_roles: List[str]) -> bool:
        # UPDATED: Both admin_main and admin_group can create meetings
        return any(role in user_roles for role in Permissions.ANY_ADMIN)
    
    @staticmethod
    def can_approve_agenda(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ADMIN_MAIN)
    
    @staticmethod
    def can_add_agenda(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ANY_ADMIN)
    
    @staticmethod
    def can_upload_file(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ANY_ADMIN)
    
    @staticmethod
    def can_edit_before_close(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ANY_ADMIN)
    
    @staticmethod
    def can_close_meeting(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ADMIN_MAIN)
    
    @staticmethod
    def can_manage_reports(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ADMIN_MAIN)
    
    @staticmethod
    def can_search_reports(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ALL_ROLES)
    
    @staticmethod
    def can_view_agenda(user_roles: List[str]) -> bool:
        return any(role in user_roles for role in Permissions.ALL_ROLES)