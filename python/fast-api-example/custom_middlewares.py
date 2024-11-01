from fastapi import Request
from fastapi.middleware.base import BaseHTTPMiddleware

# Custom middleware
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Before request
        print("FastAPI: Before request processing")
        
        # Process request through route handlers
        response = await call_next(request)
        
        # After request
        print("FastAPI: After request processing")
        return response