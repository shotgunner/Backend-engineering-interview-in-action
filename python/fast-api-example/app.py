# All Possible Imports
from fastapi import FastAPI, Path, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional
import time
import jwt
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


app = FastAPI(title='FastAPI APP')

# CORS middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Compression middleware for response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Authentication middleware
@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    try:
        # Get token from header
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
            # Verify JWT token (example)
            # jwt.decode(token, 'secret_key', algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid authentication token"}
        )
    return await call_next(request)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Error handling middleware
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

# Logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Log request details
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    # Log response details
    print(f"Response Status: {response.status_code}")
    return response


@app.get("/")
def index():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)