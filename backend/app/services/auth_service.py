from sqlalchemy.orm import Session
from app.models.user import User
#from app.models.role import Role, UserRole
from app.models import Role, UserRole

def create_dummy_users(db: Session):
    """Create dummy users for testing"""
    
    # Create roles if they don't exist
    roles_data = [
        {"role_name": "Admin ใหญ่", "description": "ผู้ดูแลระบบหลัก"},
        {"role_name": "Admin กลุ่มงาน", "description": "ผู้ดูแลกลุ่มงาน"},
        {"role_name": "ผู้ใช้ทั่วไป", "description": "ผู้ใช้งานทั่วไป"}
    ]
    
    for role_data in roles_data:
        existing_role = db.query(Role).filter(Role.role_name == role_data["role_name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
    
    db.commit()
    
    # Create dummy users if they don't exist
    users_data = [
        {
            "username": "admin",
            "fullname": "ผู้ดูแลระบบ",
            "department": "IT",
            "email": "admin@hospital.local",
            "role": "Admin ใหญ่"
        },
        {
            "username": "group_admin",
            "fullname": "นายสมชาย ใจดี",
            "department": "การพยาบาล",
            "email": "somchai@hospital.local",
            "role": "Admin กลุ่มงาน"
        },
        {
            "username": "user1",
            "fullname": "นางสาวมาลี สวยงาม",
            "department": "เภสัชกรรม",
            "email": "malee@hospital.local",
            "role": "ผู้ใช้ทั่วไป"
        }
    ]
    
    for user_data in users_data:
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing_user:
            # Create user
            user = User(
                username=user_data["username"],
                fullname=user_data["fullname"],
                department=user_data["department"],
                email=user_data["email"]
            )
            db.add(user)
            db.flush()  # Get user_id
            
            # Assign role
            role = db.query(Role).filter(Role.role_name == user_data["role"]).first()
            if role:
                user_role = UserRole(user_id=user.user_id, role_id=role.role_id)
                db.add(user_role)
    
    db.commit()
    return True