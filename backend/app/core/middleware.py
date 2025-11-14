"""
Security middleware for FastAPI application
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import time

# Rate limiting storage (in-memory, use Redis in production)
login_attempts = defaultdict(list)
RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 300  # 5 minutes in seconds

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting for login attempts
    """
    async def dispatch(self, request: Request, call_next):
        # Only apply rate limiting to login endpoint
        if request.url.path == "/api/v1/auth/login" and request.method == "POST":
            client_ip = request.client.host
            
            # Clean old attempts
            current_time = time.time()
            login_attempts[client_ip] = [
                attempt_time for attempt_time in login_attempts[client_ip]
                if current_time - attempt_time < RATE_LIMIT_WINDOW
            ]
            
            # Check rate limit
            if len(login_attempts[client_ip]) >= RATE_LIMIT_ATTEMPTS:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": f"Too many login attempts. Please try again in {RATE_LIMIT_WINDOW // 60} minutes."
                    }
                )
            
            # Record this attempt
            login_attempts[client_ip].append(current_time)
        
        response = await call_next(request)
        return response

def sanitize_error_message(error: Exception) -> str:
    """
    Sanitize error messages to avoid exposing internal details
    """
    error_str = str(error)
    
    # List of sensitive patterns to hide
    sensitive_patterns = [
        "password",
        "token",
        "secret",
        "key",
        "database",
        "connection",
        "traceback",
        "file",
        "line"
    ]
    
    # Check if error contains sensitive information
    for pattern in sensitive_patterns:
        if pattern.lower() in error_str.lower():
            return "An internal error occurred. Please contact support."
    
    return error_str
