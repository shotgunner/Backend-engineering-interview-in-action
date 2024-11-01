from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.base import BaseHTTPMiddleware
import time
import redis
from dataclasses import dataclass
from typing import Dict, Optional
from functools import wraps
import logging

"""
Rate Limiting Best Practices - Multi-Layer Approach:

1. Edge/CDN Layer (e.g. Cloudflare, Akamai)
   - First line of defense against DDoS attacks
   - Global rate limiting across all regions
   - Blocks malicious traffic before hitting origin

2. Load Balancer/Reverse Proxy Layer (e.g. Nginx)
   - Coarse-grained rate limiting
   - IP-based throttling
   - Protects backend services
   Benefits:
   - Hardware-level performance
   - Reduces load on application servers
   - Simple configuration
   Example Nginx config:
   limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

3. Application Layer (Current Implementation)
   - Fine-grained business logic
   - User/endpoint specific limits
   - Complex rate limiting rules
   Benefits:
   - More control and flexibility
   - Access to full request context
   - Can implement custom policies

4. Database Layer
   - Connection pooling limits (e.g. max_connections=100 in PostgreSQL)
   - Query rate limiting per user/tenant
   - Query complexity limits (max joins, result size)
   - Statement timeouts (e.g. SET statement_timeout = 5000)
   - PgBouncer connection pooling
   - Resource quotas per database role
   - Throttling expensive operations (bulk inserts/updates)
   - Query caching with time-based invalidation
   - Read replica load balancing
   - Prevents DB overload and resource exhaustion

Best Practice Recommendations:
1. Implement rate limiting at multiple layers for defense in depth
2. Edge layer for DDoS protection
3. Nginx for basic IP-based throttling
4. Application layer for business rules
5. Coordinate limits between layers
6. Monitor and adjust based on traffic patterns

The current implementation should be kept as part of a comprehensive 
rate limiting strategy, not as the only layer of protection.
"""

@dataclass 
class RateLimitConfig:
    requests: int  # Number of allowed requests
    window: int   # Time window in seconds

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        self.is_open = False
        
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            
    def record_success(self):
        self.failure_count = 0
        self.is_open = False
        
    def can_proceed(self):
        if not self.is_open:
            return True
            
        if time.time() - self.last_failure_time >= self.reset_timeout:
            self.is_open = False
            self.failure_count = 0
            return True
            
        return False
    
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, config: RateLimitConfig):
        super().__init__(app)
        self.redis = redis.from_url(redis_url)
        self.config = config
        self.circuit_breaker = CircuitBreaker()
        
    async def dispatch(self, request: Request, call_next):
        # Use IP + endpoint as rate limit key
        key = f"{request.client.host}:{request.url.path}"
        
        try:
            if not self.circuit_breaker.can_proceed():
                # Circuit is open - use fallback policy
                logging.warning("Circuit breaker open - bypassing rate limiting")
                return await call_next(request)
                
            # Check if rate limit exceeded
            current = self.redis.get(key)
            if current is not None and int(current) >= self.config.requests:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )
                
            # Update request count
            pipe = self.redis.pipeline()
            pipe.incr(key)
            # Set expiry if key is new
            pipe.expire(key, self.config.window)
            pipe.execute()
            
            self.circuit_breaker.record_success()
            
        except redis.RedisError as e:
            # Record Redis failure
            self.circuit_breaker.record_failure()
            logging.error(f"Redis error: {str(e)}")
            # Fallback - allow request to proceed
            return await call_next(request)
            
        return await call_next(request)

# Example usage
app = FastAPI()

rate_limit_config = RateLimitConfig(
    requests=100,    # 100 requests
    window=3600     # per hour
)

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    redis_url="redis://localhost:6379",
    config=rate_limit_config
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
Key considerations for distributed systems:

1. Use Redis/distributed cache instead of local memory
   - Ensures consistent rate limiting across multiple app instances
   - Redis pipelines ensure atomic execution of multiple commands

2. Consider using sliding window algorithm
   - More accurate than fixed window
   - Prevents burst traffic at window boundaries

3. Add buffer for clock drift between servers
   - Small grace period in time windows
   - NTP synchronization

4. Handle Redis failures gracefully
   - Circuit breaker pattern
   - Fallback policies

5. Scale considerations
   - Redis cluster for high throughput
   - Separate rate limit policies for different endpoints
   - User-based vs IP-based limiting
"""
