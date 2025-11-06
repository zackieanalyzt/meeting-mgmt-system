from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    fullname = Column(String(100))
    department = Column(String(100))
    email = Column(String(100))