"""
Audit logging system for security events
"""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure audit logger
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# File handler for audit logs
audit_handler = logging.FileHandler(LOGS_DIR / "audit.log")
audit_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
audit_handler.setFormatter(formatter)
audit_logger.addHandler(audit_handler)

def log_login_success(username: str, ip_address: str):
    """Log successful login attempt"""
    audit_logger.info(f"LOGIN_SUCCESS | user={username} | ip={ip_address}")

def log_login_failure(username: str, ip_address: str, reason: str = "Invalid credentials"):
    """Log failed login attempt"""
    audit_logger.warning(f"LOGIN_FAILURE | user={username} | ip={ip_address} | reason={reason}")

def log_meeting_create(username: str, meeting_id: int, meeting_title: str):
    """Log meeting creation"""
    audit_logger.info(f"MEETING_CREATE | user={username} | meeting_id={meeting_id} | title={meeting_title}")

def log_meeting_update(username: str, meeting_id: int, meeting_title: str):
    """Log meeting update"""
    audit_logger.info(f"MEETING_UPDATE | user={username} | meeting_id={meeting_id} | title={meeting_title}")

def log_meeting_delete(username: str, meeting_id: int, meeting_title: str):
    """Log meeting deletion"""
    audit_logger.warning(f"MEETING_DELETE | user={username} | meeting_id={meeting_id} | title={meeting_title}")

def log_meeting_close(username: str, meeting_id: int, meeting_title: str):
    """Log meeting closure"""
    audit_logger.info(f"MEETING_CLOSE | user={username} | meeting_id={meeting_id} | title={meeting_title}")

def log_unauthorized_access(username: Optional[str], ip_address: str, endpoint: str):
    """Log unauthorized access attempt"""
    user = username or "anonymous"
    audit_logger.warning(f"UNAUTHORIZED_ACCESS | user={user} | ip={ip_address} | endpoint={endpoint}")

def log_security_event(event_type: str, details: str):
    """Log general security event"""
    audit_logger.warning(f"SECURITY_EVENT | type={event_type} | details={details}")
