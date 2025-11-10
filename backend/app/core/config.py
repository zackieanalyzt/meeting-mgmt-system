from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    POSTGRES_HOST: str = "192.168.100.70"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "meeting_mgmt"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "grespost"
    
    MARIADB_HOST: str = "192.168.100.170"
    MARIADB_PORT: int = 3306
    MARIADB_DB: str = "hr"
    MARIADB_USER: str = "root"
    MARIADB_PASSWORD: str = "cjv671"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    UPLOAD_PATH: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()