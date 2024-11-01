"""
Key differences between synchronous frameworks like Flask and asynchronous ones like FastAPI:

1. Request Handling:
- Flask: Synchronous, handles one request at a time per worker
- FastAPI: Asynchronous, can handle multiple requests concurrently using async/await

2. Performance:
- Flask: Better for CPU-bound tasks and simple applications
- FastAPI: Better for I/O-bound tasks and high-concurrency scenarios

3. Blocking I/O Operations:

Flask Example - Blocking:
"""
from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def sync_endpoint():
    # Blocks the worker until response is received
    response = requests.get("https://api.example.com/data")
    return response.json()

"""
Flask with Background Tasks:
- Use Celery/Redis for async operations
- Use threading/multiprocessing
- Use event loops like gevent

FastAPI Example - Non-blocking:
"""
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def async_endpoint():
    # Non-blocking - other requests can be processed while waiting
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

"""
4. Development Experience:
- Flask: Simple, straightforward, great for learning
- FastAPI: Modern features like type hints, automatic API docs

5. Use Cases:
- Flask: Simple web apps, APIs, microservices with moderate traffic
- FastAPI: High-performance APIs, real-time applications, microservices with high concurrency
"""
