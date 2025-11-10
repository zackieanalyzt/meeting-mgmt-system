import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, text

# === MariaDB Connection Info ===
MARIADB_HOST = "192.168.100.170"
MARIADB_PORT = 3306
MARIADB_DB = "hr"
MARIADB_USER = "root"
MARIADB_PASSWORD = "cjv671"

# =====================================
mariadb_url = (
    f"mysql+pymysql://{MARIADB_USER}:{MARIADB_PASSWORD}"
    f"@{MARIADB_HOST}:{MARIADB_PORT}/{MARIADB_DB}"
)

print("🔧 Connecting to:", mariadb_url)

try:
    engine = create_engine(mariadb_url)
    with engine.connect() as conn:
        version = conn.execute(text("SELECT VERSION();")).scalar()
        print("✅ MariaDB connected successfully!")
        print("   Version:", version)

        # ทดสอบอ่านข้อมูลจาก hr.personnel
        try:
            rows = conn.execute(text("SELECT username FROM hr.personnel LIMIT 5;")).fetchall()
            if not rows:
                print("⚠️ Table hr.personnel is empty or no data returned.")
            else:
                print("👥 Sample usernames from hr.personnel:")
                for r in rows:
                    print("   ", r[0])
        except Exception as suberr:
            print("⚠️ Connected but couldn't query hr.personnel:", suberr)

except Exception as e:
    print("❌ Connection failed:")
    print(e)
