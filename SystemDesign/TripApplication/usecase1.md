# Polarsteps Technical Interview Design (75 minutes)

## Part 1: Technical Discussion (20 minutes)

### Questions about HTTP, REST, DB optimization, and caching:

#### Request/Response Cycle
- "Walk me through what happens when a user enters polarsteps.com in their browser"
  1. DNS Resolution:
     - Browser checks local DNS cache
     - If not found, queries DNS servers to resolve polarsteps.com to IP address
     - DNS lookup follows hierarchy: local cache → ISP DNS → root DNS → TLD DNS → authoritative DNS

  2. TCP Connection:
     - Browser initiates TCP 3-way handshake with server IP
     - SYN → SYN-ACK → ACK
     - Establishes reliable connection

  3. TLS/SSL Handshake (HTTPS):
     - Client hello with supported cipher suites
     - Server hello with chosen cipher suite
     - Certificate verification
     - Key exchange for encrypted communication

  4. HTTP Request:
     - Browser sends GET request to server
     - Includes headers (User-Agent, Accept, etc.)
     - Any cookies for polarsteps.com domain

  5. Server Processing:
     - Load balancer routes request
     - Web server receives request
     - Application logic processes request
     - Database queries if needed
     - Generates HTML response

  6. Response & Rendering:
     - Server sends HTTP response with HTML/CSS/JS
     - Browser parses HTML
     - Downloads additional assets (images, scripts)
     - Renders page progressively
     - Executes JavaScript
  
- "How would you handle request timeouts in a distributed system?"
  1. Circuit Breaker Pattern:
     - Monitor failed requests
     - Trip circuit after threshold reached
     - Prevent cascading failures
     - Allow periodic retry attempts

  2. Timeout Configuration:
     - Set appropriate timeout values
     - Consider network latency
     - Different timeouts for different services
     - Exponential backoff for retries

  3. Fallback Mechanisms:
     - Cache responses for critical paths
     - Degrade gracefully with default values
     - Queue requests for retry
     - Return partial results when possible

  4. Monitoring & Alerting:
     - Track timeout frequency
     - Alert on timeout spikes
     - Monitor service health
     - Log timeout patterns

  5. Request Tracing:
     - Implement distributed tracing
     - Track request lifecycle
     - Identify bottlenecks
     - Debug timeout issues
  
- "Explain how you would implement rate limiting for an API"
  1. Token Bucket Algorithm:
     - Assign tokens per time window:
     - Each request consumes a token
     - Tokens replenish at fixed rate
     - Reject when bucket empty
       ```python
       # Server-side rate limiter
       class RateLimiter:
           def __init__(self, tokens_per_min=100):
               self.tokens_per_min = tokens_per_min
               self.buckets = {}  # user_id -> bucket
               
           def allow_request(self, user_id):
               if user_id not in self.buckets:
                   self.buckets[user_id] = {
                       'tokens': self.tokens_per_min,
                       'last_refill': time.time()
                   }
               return self._check_token(user_id)
        
           def _check_token(self, user_id):
                bucket = self.buckets[user_id]
                now = time.time()
                time_passed = now - bucket['last_refill']
                
                # Refill tokens based on time passed
                new_tokens = int(time_passed * (self.tokens_per_min / 60.0))
                bucket['tokens'] = min(
                    self.tokens_per_min,  # Cap at max tokens
                    bucket['tokens'] + new_tokens
                )
                bucket['last_refill'] = now
                
                # Check if request can be allowed
                if bucket['tokens'] >= 1:
                    bucket['tokens'] -= 1
                    return True
                return False

       # Client-side handling
       def api_request(url, user_id):
           response = requests.get(
               url,
               headers={'X-User-ID': user_id}
           )
           if response.status_code == 429:  # Rate limited
               retry_after = int(response.headers['Retry-After'])
               time.sleep(retry_after)
               return api_request(url, user_id)  # Retry
           return response
       ```


  1. Implementation Options:
     - Redis for distributed systems
     - In-memory for single server
     - Track by IP/API key/user
     - Configure limits per endpoint

  2. Response Headers:
     - Return remaining quota
     - Include reset timestamp
     - HTTP 429 when limit exceeded
     - Retry-After header

  3. Rate Limit Rules:
     - Different tiers for users
     - Burst allowance
     - Geographic considerations 
     - Time-based variations

  4. Monitoring & Alerts:
     - Track rate limit hits
     - Alert on abuse patterns
     - Monitor performance impact
     - Analyze usage trends

#### Database Indexes
- B-tree vs Hash index choice depends on query patterns:
  - B-tree indexes:
    - Range queries (e.g. date ranges, price ranges)
    - Prefix searches
    - Ordered results
    - Support multiple columns
    - More space efficient
    Example:
    ```sql
    CREATE INDEX btree_idx ON orders (order_date);
    -- Efficient for:
    SELECT * FROM orders 
    WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';
    ```

  - Hash indexes:
    - Exact match lookups only
    - Faster point queries (O(1) vs O(log n))
    - Single column only
    - Not suitable for ranges/sorting
    - More memory intensive
    Example:
    ```sql
    CREATE INDEX hash_idx ON users USING HASH (email);
    -- Efficient for:
    SELECT * FROM users WHERE email = 'user@example.com';
    ```
  - GiST (Generalized Search Tree) indexes:
    - Optimized for geometric/spatial data
    - Support complex data types
    - Excellent for geospatial queries
    - Handle containment, intersection, proximity
    - Used with PostGIS extension
    Example:
    ```sql
    CREATE INDEX gist_idx ON locations USING GIST (coordinates);
    -- Efficient for:
    SELECT * FROM locations 
    WHERE coordinates && ST_MakeEnvelope(lon1,lat1,lon2,lat2);
    ```

  - BRIN (Block Range INdex) indexes:
    - For very large tables with correlated values
    - Much smaller than B-tree
    - Good for time-series or sequential data
    - Lower maintenance overhead
    - Trade speed for size
    Example:
    ```sql
    CREATE INDEX brin_idx ON events USING BRIN (timestamp);
    -- Good for:
    SELECT * FROM events 
    WHERE timestamp >= '2023-01-01';
    ```

  - GIN (Generalized Inverted Index) indexes:
    - Full-text search
    - Array containment
    - JSON document indexing
    - Multiple values per row
    - Slower updates but faster searches
    Example:
    ```sql
    CREATE INDEX gin_idx ON posts USING GIN (tags);
    -- Efficient for:
    SELECT * FROM posts WHERE tags @> ARRAY['travel'];
    ```

  - Partial indexes:
    - Index subset of rows
    - Smaller size
    - Faster maintenance
    - Useful for filtered queries
    Example:
    ```sql
    CREATE INDEX partial_idx ON orders (order_date) 
    WHERE status = 'active';
    -- Optimized for:
    SELECT * FROM orders 
    WHERE status = 'active' AND order_date > '2023-01-01';
    ```

  Why this matters:
  - Wrong index type can severely impact query performance
  - B-trees are more versatile but slightly slower for exact matches
  - Hash indexes excel at lookups but lack range support
  - Memory/storage constraints may influence choice
  - Query patterns should drive index selection
- "How would you design indexes for a query that filters trips by date range and location?"
- "Explain the trade-offs between adding indexes and write performance"

#### Caching
- "How would you implement caching for frequently accessed trip data?"
  - Use Redis as distributed cache layer:
    - Store trip data in hash structures
    - Set appropriate TTL based on update frequency
    - Cache most viewed trips
    Example:
    ```redis
    HSET trip:123 title "Europe Tour" description "..." views 1000
    EXPIRE trip:123 3600
    ```
  
  - Multi-level caching strategy:
    - Application-level cache (in-memory)
    - Distributed cache (Redis)
    - Database as source of truth
    
  - Cache invalidation approach:
    - Write-through: Update cache and DB together
    ```python
    from functools import wraps
    from redis import Redis
    
    redis_client = Redis(host='localhost', port=6379)
    
    def invalidate_cache(key_pattern):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                # Execute the original function/method
                result = f(*args, **kwargs)
                
                # Invalidate cache based on pattern
                keys = redis_client.keys(key_pattern)
                if keys:
                    redis_client.delete(*keys)
                    
                return result
            return wrapper
        return decorator
        
    # Example usage:
    @invalidate_cache("trip:*")
    def update_trip(trip_id, data):
        # Update DB
        db.session.query(Trip).filter_by(id=trip_id).update(data)
        db.session.commit()
    ```
    - Set reasonable TTL to auto-expire
    - Invalidate on trip updates using decorator pattern
    
  - Cache warming considerations:
    - Pre-cache popular trips
    - Background job to maintain hot data
    - Monitor cache hit rates
- "Explain cache invalidation strategies you'd use for user profile updates"
  - Time-based invalidation:
    ```redis
    # Cache user profile with TTL
    SETEX user:123:profile 3600 "{name: 'John', email: 'john@example.com'}"
    ```
  
  - Event-driven invalidation:
    - Invalidate on profile updates using Redis Pub/Sub
    ```python
    from flask import Flask, jsonify
    from redis import Redis
    import threading
    
    app = Flask(__name__)
    redis_client = Redis(host='localhost', port=6379)
    
    # Publisher endpoint
    @app.route('/api/users/<int:user_id>/profile', methods=['PUT'])
    def update_profile(user_id):
        # Update profile in database
        # ...
        
        # Publish update event
        redis_client.publish('profile_updates', user_id)
        return jsonify({'message': 'Profile updated successfully'})
    
    # Subscriber setup
    def start_subscriber():
        pubsub = redis_client.pubsub()
        pubsub.subscribe('profile_updates')
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                user_id = message['data']
                # Invalidate cache
                redis_client.delete(f'user:{user_id}:profile')
    
    # Start subscriber in background thread
    subscriber_thread = threading.Thread(target=start_subscriber)
    subscriber_thread.daemon = True
    subscriber_thread.start()
    ```
  
  - Selective field invalidation:
    - Only invalidate affected fields using Redis hashes
    ```redis
    # Store profile fields separately
    HSET user:123:profile name "John" email "john@example.com"
    # Update single field
    HDEL user:123:profile email
    ```
    
  - Versioning strategy:
    - Maintain version number for profiles
    ```python
    # Increment version on update
    redis_client.incr(f'user:{user_id}:version')
    
    # Check version when reading cache
    def get_profile(user_id):
        cache_version = redis_client.get(f'user:{user_id}:version')
        cached_profile = redis_client.get(f'user:{user_id}:profile')
        if cached_profile and cached_profile['version'] == cache_version:
            return cached_profile
        return refresh_cache(user_id)
    ```
- "Compare Redis vs Memcached for our use case"

## Part 2: System Design (30 minutes)

### Design a feature for Polarsteps' trip tracking system:

**Problem:** Design a system that allows users to share their real-time location during trips, with the following requirements:

- Support millions of active travelers
- Location updates every 5 minutes
- Ability to share trips with specific friends/family
- Show nearby points of interest
- Work in areas with poor connectivity

**Expected discussion points:**
- Data model design
- API design
- Scaling considerations
- Offline functionality
- Privacy concerns

Answer:



## Part 3: Coding Exercise (25 minutes)

### Implement 3 REST endpoints for the trip-sharing feature:

**Key aspects to evaluate:**
- Input validation
- Error handling
- Database queries optimization
- Rate limiting consideration
- Security measures

### This interview structure tests:
- System design capabilities
- REST API design
- Database knowledge
- Caching strategies
- Real-world problem solving
- Code organization
- Security awareness

*The difficulty level is medium-hard because it combines theoretical knowledge with practical implementation, and requires understanding of scalability and performance optimization.*