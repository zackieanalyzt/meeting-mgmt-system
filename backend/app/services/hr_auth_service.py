from sqlalchemy import text
from app.core.database import MariaDBSessionLocal
import hashlib

def verify_hr_user(username: str, password: str) -> bool:
    """
    ตรวจสอบผู้ใช้จากฐาน hr.personnel (MariaDB)
    โดยเข้ารหัส password ด้วย MD5 ก่อนเปรียบเทียบ
    """
    with MariaDBSessionLocal() as db:
        # แปลงรหัสผ่านที่รับเข้ามาให้เป็น MD5 hash ก่อนตรวจสอบ
        hashed_pw = hashlib.md5(password.encode()).hexdigest()

        query = text("""
            SELECT COUNT(*) FROM hr.personnel
            WHERE username = :u AND password = :p
        """)
        result = db.execute(query, {"u": username, "p": hashed_pw}).scalar()
        print(f"[DEBUG] username={username}, input_pw={password}, hashed={hashed_pw}, result={result}")
        return result and result > 0
