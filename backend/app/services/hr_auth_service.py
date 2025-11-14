from sqlalchemy import text
from app.core.database import MariaDBSessionLocal
from app.core.security import verify_password

def verify_hr_user(username: str, password: str) -> bool:
    """
    ตรวจสอบผู้ใช้จากฐาน hr.personnel (MariaDB)
    รองรับทั้ง MD5 (legacy) และ bcrypt (secure)
    """
    with MariaDBSessionLocal() as db:
        query = text("""
            SELECT password FROM hr.personnel
            WHERE TRIM(username) = :u
            LIMIT 1
        """)
        result = db.execute(query, {"u": username}).fetchone()
        
        if not result:
            return False
        
        stored_hash = result[0]
        return verify_password(password, stored_hash)
