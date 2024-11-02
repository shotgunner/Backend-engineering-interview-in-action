# Redis Interview Questions for Senior Backend Engineer

---

## Practical/Hands-on Questions

### Data Structure Scenarios

#### Q1: Real-Time User Ranking System Based on Points

**Scenario:** Rank 1 million users based on their game scores.

**Requirements:**

- Fast score updates
- Quick retrieval of user ranks
- Get top N players
- Get nearby ranks for a user

**Solution Using Sorted Sets (ZSET):**

```redis
# Add/update user score
ZADD leaderboard 1000 user:123   # User 123 has 1000 points, O(log N)
ZADD leaderboard 2000 user:456   # User 456 has 2000 points

# Get user's rank (0-based)
ZREVRANK leaderboard user:123    # O(log N)

# Get top 10 players
ZREVRANGE leaderboard 0 9 WITHSCORES

# Get users around player's rank (e.g., 5 above and below)
ZREVRANGE leaderboard BY SCORE LIMIT -5 5
```

**Notes:**

- **Sorted Sets (ZSETs):** Uses both a skip list (O(log N) for ordering) and a hash table (O(1) lookups by member).

---

#### Q2: Social Media Follow/Following System

**Scenario:** Track user relationships, i.e., who follows whom.

**Requirements:**

- Track who follows whom
- Fast lookups for followers/following
- Check if user A follows user B

**Solution Using Sets:**

```redis
# User 123 follows user 456
SADD following:123 456   # Add to 123's following set
SADD followers:456 123   # Add to 456's followers set

# Check if 123 follows 456
SISMEMBER following:123 456

# Get all followers/following
SMEMBERS followers:456
SMEMBERS following:123
```

---

#### Q3: User Session Store

**Scenario:** Store user session data with automatic expiration.

**Requirements:**

- Store multiple fields per session
- Automatic expiration
- Fast field updates
- Atomic operations

**Solution Using Hashes with Expiration:**

```redis
# Create session with multiple fields
HSET session:xyz123 user_id 456 login_time "2023-01-01" status "active"
EXPIRE session:xyz123 3600    # Expires in 1 hour

# Update single field
HSET session:xyz123 status "idle"

# Get specific field or all fields
HGET session:xyz123 status
HGETALL session:xyz123
```

---

#### Q4: Time-Series Event Log

**Scenario:** Store the latest 1000 events per user.

**Requirements:**

- Fixed size storage
- Chronological order
- Automatic old event removal

**Solution Using Lists with Capped Size:**

```redis
# Add new event (prepend)
LPUSH user:123:events "logged_in:2023-01-01"

# Trim to keep only the latest 1000
LTRIM user:123:events 0 999

# Get latest 10 events
LRANGE user:123:events 0 9
```

---

## Advanced Design Questions

### 1. Distributed Rate Limiter

**Scenario:** Implement a rate limiter for 10,000 requests/second with a Redis cluster (3 master and 3 replica nodes).

**Considerations:**

- **Rate Limiting Algorithm Choice:** Use a token bucket or leaky bucket algorithm to efficiently limit requests.
- **Key Design and TTL Strategy:** Use a unique key for each client/requestor with an appropriate TTL to control the rate limit window.
- **Lua Scripting for Atomicity:** Use Lua scripts to ensure atomic operations across multiple Redis commands.
- **Node Failure Handling:** Use Redis Sentinel or Cluster for failover to ensure availability during node failures.
- **Monitoring for Performance:** Monitor Redis keyspace and memory usage using Redis monitoring tools like Redis Insights or custom scripts.

---

### 2. Real-Time Leaderboard System

**Scenario:** Handle 1M+ users, real-time score updates, and pagination.

**Key Points:**

- **Sorted Set Operations:** Use Redis sorted sets (ZSET) for efficient ranking and score updates.
- **Memory vs Performance Trade-Offs:** Use compression and tune the maxmemory setting for an optimal balance between memory and performance.
- **Sharding Strategy:** Use consistent hashing to distribute users across multiple Redis instances.
- **Caching Layers:** Implement a caching layer in front of Redis to reduce direct hits and improve response times.
- **Data Persistence:** Use AOF (Append Only File) with appropriate fsync policies to maintain data durability without compromising performance.

---

### 3. Distributed Locking Mechanism

**Scenario:** Design a locking mechanism resistant to network partitions, process crashes, and clock drift.

**Implementation Considerations:**

- **Lock Acquisition Algorithm:** Use the Redlock algorithm to ensure distributed lock safety and correctness.
- **Heartbeat Mechanism:** Implement a heartbeat to extend the lock if the process is still active.
- **Automatic Lock Release:** Set a TTL for automatic lock expiration to avoid deadlocks.
- **Replication Consistency:** Use Redis replication to ensure the lock is consistently replicated across nodes.
- **Failure Recovery:** Implement fallback mechanisms in case of lock acquisition failures or node crashes.

---

### 4. Debugging Redis Latency Spikes

**Scenario:** Address significant latency spikes in a Redis cluster during peak hours.

**Technical Areas to Cover:**

- **Identify Bottlenecks:** Use Redis slow logs to identify long-running commands.
- **Slow Log Analysis:** Analyze slow logs and identify the commands causing delays.
- **Monitor Key Metrics:** Monitor key metrics such as CPU usage, memory usage, and network latency.
- **Memory Fragmentation:** Check for memory fragmentation and consider using `MEMORY PURGE` to reduce fragmentation.
- **Command Optimization:** Optimize commands by reducing the complexity and frequency of expensive operations.
- **Cluster Rebalancing:** Redistribute data across cluster nodes to balance the load and reduce latency.

---

### 5. Caching System Design

**Scenario:** Implement a caching system with Redis that handles cache invalidation, write-through/write-behind, hot key protection, and memory eviction.

**Design Aspects:**

- **Cache Coherence Strategy:** Use a combination of write-through and write-behind caching to ensure consistency.
- **Eviction Policies:** Use Redis eviction policies like LRU (Least Recently Used) or LFU (Least Frequently Used) to manage memory efficiently.
- **Key Design Patterns:** Use namespacing and consistent key patterns to organize cached data.
- **Monitoring and Alerts:** Set up monitoring to track cache hit/miss ratios and configure alerts for high miss rates.
- **Failure Scenarios:** Implement retries and fallbacks in case of cache server failures to ensure system resilience.

---

## Theoretical Questions

### 6. Redis Persistence Options

**Question:** Compare Redis persistence options (RDB vs AOF) and explain when you'd choose each.

**Answer:**

- **RDB (Redis Database Backup):**

  - **Performance Impact:** RDB snapshots are less frequent, leading to minimal performance overhead.
  - **Data Consistency Guarantees:** Data loss may occur since snapshots are taken periodically.
  - **Recovery Scenarios:** Faster recovery time as entire datasets are loaded at once.
  - **Use Case:** Suitable for use cases where fast recovery is essential, but some data loss is acceptable.

- **AOF (Append Only File):**

  - **Performance Impact:** More write-intensive, especially if `fsync` is set to `always`.
  - **Data Consistency Guarantees:** Provides better durability; logs every write operation.
  - **Recovery Scenarios:** More granular recovery, but slower compared to RDB.
  - **Use Case:** Suitable for applications requiring minimal data loss and better durability guarantees.

- **Hybrid Approach:** Use both RDB and AOF to balance between durability and performance, ensuring snapshots for quick recovery and AOF for durability.

---

### 7. Redis Cluster Architecture and Data Sharding Strategies

**Question:** Explain Redis cluster architecture and data sharding strategies.

**Answer:**

- **Hash Slots:** Redis cluster uses 16,384 hash slots to distribute data across nodes. Each key is assigned a hash slot, and nodes manage these slots.
- **Node Addition/Removal:** When a node is added or removed, hash slots are reallocated to maintain balance. This is handled using the `reshard` command.
- **Resharding Process:** During resharding, data is moved from one node to another without interrupting the cluster.
- **Cross-Slot Operations:** Operations involving multiple keys (e.g., transactions) must reside in the same hash slot or use hash tags to ensure atomicity.

---

### 8. Redis Data Structures and Memory Optimization Techniques

**Question:** Describe Redis data structures internals and memory optimization techniques.

**Answer:**

- **String Encoding:** Redis optimizes memory usage by using different encodings like `int`, `embstr`, and `raw` based on the content of the string.
- **List/Hash/Set Implementations:**
  - **List:** Uses linked lists or ziplist based on the size and number of elements.
  - **Hash:** Uses hash tables or ziplist based on the number of fields and size of the values.
  - **Set:** Uses hash tables or intset depending on the number and type of elements.
- **Memory Fragmentation:** Reduce fragmentation by periodically using `MEMORY PURGE` and ensuring appropriate maxmemory settings.
- **Compression Strategies:** Use `redis.conf` settings to compress values and use efficient encodings to save memory.

---

### 9. Redis Transactions and Atomic Operations

**Question:** Explain Redis transactions in detail and demonstrate how you would implement atomic operations for a real-world scenario.

**Answer:**

- **MULTI/EXEC Pipeline:** Redis transactions are initiated with `MULTI`, commands are queued, and executed atomically with `EXEC`.
- **Optimistic Locking with WATCH:** Use `WATCH` to monitor keys for changes before starting a transaction, ensuring atomicity.
- **Error Handling:** Handle transaction failures due to key modifications using retry mechanisms.
- **Race Conditions:** WATCH helps prevent race conditions by aborting transactions if watched keys are modified.

**Example Scenario:** Implementing atomic inventory updates with error handling.

**Technical Considerations:**

- **Network Failures:** Handle retries and ensure that operations are idempotent.
- **Client Timeout Handling:** Set appropriate timeouts to avoid long waits during network issues.
- **Memory Usage:** Monitor memory usage to ensure transactions do not exhaust memory.
- **Command Ordering:** Ensure commands are ordered logically within the transaction to maintain consistency.
- **Performance Impact:** Minimize the number of commands in a transaction to reduce latency.

```python
# Using Python redis-py client
def update_inventory(redis_conn, product_id, quantity):
    # Watch the inventory key for changes
    inventory_key = f"inventory:{product_id}"
    redis_conn.watch(inventory_key)
    
    try:
        # Get current inventory
        current_stock = int(redis_conn.get(inventory_key) or 0)
        
        # Check if we have enough stock
        if current_stock < quantity:
            redis_conn.unwatch()
            return False
            
        # Start transaction
        pipe = redis_conn.pipeline()
        pipe.multi()
        
        # Queue inventory update
        new_stock = current_stock - quantity
        pipe.set(inventory_key, new_stock)
        
        # Queue order tracking
        pipe.rpush(f"orders:{product_id}", 
                  f"order:{quantity}:{timestamp}")
                  
        # Execute transaction
        pipe.execute()
        return True
        
    except WatchError:
        # Another client modified the key
        return False
        
    finally:
        pipe.reset()
```

---

Each question and solution aims to evaluate both practical implementation skills and deep theoretical knowledge required for senior backend positions.


# Redis Interview Questions for Senior Backend Engineer

---

## Practical/Hands-on Questions

### Pub/Sub vs Stream in Redis

#### Q1: Pub/Sub - Real-Time Messaging

**Scenario:** Use Redis Pub/Sub to implement a simple chat application where multiple users receive messages in real time.

**Requirements:**

- Instantaneous message delivery to all connected subscribers
- No message persistence (messages are only sent to currently connected clients)

**Solution Using Pub/Sub:**

```redis
# Publish a message to a channel
PUBLISH chat_room "Hello, everyone!"

# Subscribe to a channel
SUBSCRIBE chat_room
```

**Notes:**

- **Pub/Sub** in Redis is suitable for real-time notifications where subscribers only receive messages if they're connected at the time of publication.
- **No Message Persistence:** Messages are not stored. Once a message is published, it’s only received by subscribers currently connected to the channel.
- **Use Cases:** Ideal for lightweight, real-time messaging where historical data isn’t required (e.g., live chat, notifications).

---

#### Q2: Stream - Reliable Event Logging with Persistence

**Scenario:** Use Redis Streams to log user activity for a web application and replay events later for analytics.

**Requirements:**

- Persisted message storage, allowing messages to be read even after publishing
- Replay capability to process or analyze events after they occur

**Solution Using Streams:**

```redis
# Add an event to a stream
XADD user_activity * user_id 123 event "page_view"

# Read events from the stream
XRANGE user_activity - +
```

**Notes:**

- **Redis Streams** store messages persistently, allowing for historical reads and replaying messages.
- **Message Persistence:** Messages remain in the stream until explicitly deleted, enabling delayed or repeat processing.
- **Use Cases:** Ideal for applications requiring reliable message processing, like event logging, analytics, or data pipeline implementations.

---

#### Key Differences:

- **Persistence:** Pub/Sub does not store messages, while Streams retain messages until deleted.
- **Replayability:** Streams allow you to replay and process past messages; Pub/Sub only works with real-time delivery.
- **Consumer Groups (Streams Only):** Redis Streams support consumer groups, allowing multiple consumers to process messages in parallel without duplication.
- **Use Case Fit:** Pub/Sub is best for real-time notifications; Streams suit applications needing message durability and reliable processing.

