# Technical Interview Questions for Polarsteps Backend Position

# Request/Response Cycle Questions
#1. "In FastAPI/Flask/django, explain the lifecycle of a request from when it hits your API endpoint to the response being sent back. Include middleware handling."

# FastAPI Example
from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware

app = FastAPI()

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

app.add_middleware(TimingMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Flask Example
from flask import Flask, request, g
from functools import wraps

flask_app = Flask(__name__)

def timing_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Before request
        print("Flask: Before request processing")
        
        # Process request
        response = f(*args, **kwargs)
        
        # After request
        print("Flask: After request processing")
        return response
    return decorated_function

@flask_app.route('/')
@timing_middleware
def hello():
    return {'message': 'Hello World'}

# Django Example
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class TimingMiddlewareDjango(MiddlewareMixin):
    def process_request(self, request):
        # Before request
        print("Django: Before request processing")
        
    def process_response(self, request, response):
        # After request
        print("Django: After request processing")
        return response

# In Django views.py
def home(request):
    return JsonResponse({'message': 'Hello World'})

"""
Key Differences in Request Lifecycle:

1. FastAPI:
- Async by default
- Middleware is processed in order of addition
- Uses Starlette's request/response cycle
- Built-in dependency injection
- Type validation via Pydantic

2. Flask:
- Synchronous by default
- Uses decorator pattern for middleware
- Simple request context
- Global 'g' object for request context
- Lightweight and minimal

3. Django:
- Full-featured framework with built-in middleware
- Multiple middleware hooks (process_request, process_view, process_response)
- Request passes through all middleware before reaching view
- Response passes back through middleware in reverse order
- Built-in session and auth middleware
"""




