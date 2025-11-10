from sqlalchemy import text
from app.core.database import MariaDBSessionLocal

def verify_hr_user(username: str, password: str) -> bool:
    """
    ตรวจสอบผู้ใช้จากฐาน hr.personnel (MariaDB)
    """
    with MariaDBSessionLocal() as db:
        query = text("""
            SELECT COUNT(*) FROM hr.personnel
            WHERE username = :u AND password = :p
        """)
        result = db.execute(query, {"u": username, "p": password}).scalar()
        return result and result > 0
