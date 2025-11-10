from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# === Base สำหรับ ORM Models ===
Base = declarative_base()

# === PostgreSQL Connection ===
POSTGRES_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
postgres_engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
PostgresSessionLocal = sessionmaker(bind=postgres_engine, autoflush=False, autocommit=False)

# === MariaDB Connection ===
MARIADB_URL = (
    f"mysql+pymysql://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}"
    f"@{settings.MARIADB_HOST}:{settings.MARIADB_PORT}/{settings.MARIADB_DB}"
)
mariadb_engine = create_engine(MARIADB_URL, pool_pre_ping=True)
MariaDBSessionLocal = sessionmaker(bind=mariadb_engine, autoflush=False, autocommit=False)

# === Dependency สำหรับ FastAPI (ใช้กับ PostgreSQL) ===
def get_db():
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()
