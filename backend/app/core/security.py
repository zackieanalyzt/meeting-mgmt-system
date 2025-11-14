"""
Security utilities for password hashing and verification
"""
import hashlib
from passlib.context import CryptContext

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Supports both bcrypt (new) and MD5 (legacy) for backward compatibility.
    """
    # Try bcrypt first (new secure method)
    try:
        if pwd_context.verify(plain_password, hashed_password):
            return True
    except Exception:
        pass
    
    # Fallback to MD5 for legacy passwords
    try:
        md5_hash = hashlib.md5(plain_password.encode()).hexdigest()
        if md5_hash == hashed_password:
            return True
    except Exception:
        pass
    
    return False

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password)

def needs_rehash(hashed_password: str) -> bool:
    """
    Check if a password hash needs to be rehashed (e.g., MD5 -> bcrypt).
    """
    # If it's 32 characters, it's likely MD5
    if len(hashed_password) == 32:
        try:
            int(hashed_password, 16)  # Check if it's hex
            return True
        except ValueError:
            pass
    
    # Check if bcrypt hash needs update
    return pwd_context.needs_update(hashed_password)
