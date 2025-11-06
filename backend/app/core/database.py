from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# PostgreSQL (Main Database)
POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MariaDB (Auth Database)
MARIADB_URL = f"mysql+pymysql://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}@{settings.MARIADB_HOST}:{settings.MARIADB_PORT}/{settings.MARIADB_DB}"

auth_engine = create_engine(MARIADB_URL)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_db():
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()