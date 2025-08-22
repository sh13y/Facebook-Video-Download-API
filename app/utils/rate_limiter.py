import time
from collections import defaultdict, deque
from typing import Dict, Deque
from fastapi import HTTPException, Request
from app.config import settings

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.clients: Dict[str, Deque[float]] = defaultdict(deque)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make request"""
        now = time.time()
        window_start = now - settings.RATE_LIMIT_WINDOW
        
        # Clean old requests
        client_requests = self.clients[client_id]
        while client_requests and client_requests[0] <= window_start:
            client_requests.popleft()
        
        # Check rate limit
        if len(client_requests) >= settings.RATE_LIMIT_REQUESTS:
            return False
        
        # Add current request
        client_requests.append(now)
        return True
    
    def get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Use X-Forwarded-For header if available (for proxy setups)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Fall back to direct client IP
        client_host = getattr(request.client, "host", "unknown")
        return client_host

# Global rate limiter instance
rate_limiter = RateLimiter()

async def check_rate_limit(request: Request):
    """Dependency to check rate limits"""
    client_id = rate_limiter.get_client_id(request)
    
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail={
                "status": "error",
                "message": f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds.",
                "error_code": "RATE_LIMIT_EXCEEDED"
            }
        )