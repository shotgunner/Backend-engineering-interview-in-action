# Data Structures Interview Questions for Senior Python Backend Engineers

## 1. Skip Lists vs B-Trees
Q: When would you choose a Skip List over a B-Tree for implementing a sorted set?
A: Skip Lists are often preferred when:
- You need simpler implementation (Redis uses Skip Lists for this reason)
- Memory overhead is less critical (Skip Lists use ~2x memory of B-Trees)
- You want lock-free concurrent access (Skip Lists are easier to make thread-safe because each node update is localized and doesn't require rebalancing, unlike B-trees which may need complex rebalancing operations affecting multiple nodes)
- Average case O(log n) performance is acceptable (B-Trees guarantee worst case)

## 2. Custom Hash Tables
Q: How would you implement a custom hash table to handle frequent collisions?
A: Key strategies include:
- Using a good hash function (like MurmurHash3)
- Implementing proper collision resolution (chaining vs open addressing)
- Dynamic resizing when load factor exceeds threshold
- Consider Robin Hood hashing for better cache performance
- Use consistent hashing for distributed systems

## 3. Concurrent Data Structures
Q: What considerations are important when implementing thread-safe data structures?
A: Critical aspects include:
- Using atomic operations where possible
- Proper lock granularity (fine-grained vs coarse-grained)
- Lock-free algorithms for better scalability
- Memory barriers and visibility
- Handling ABA problems in lock-free structures

## 4. Memory-Efficient Collections
Q: How would you optimize a collection for memory usage in Python?
A: Key techniques include:
- Using __slots__ to reduce per-instance memory
- Collections.deque for double-ended queues
- array.array for homogeneous numerical data
- bisect module for maintaining sorted lists
- weakref for cache-like structures

## 5. Time Complexity Analysis
Q: Compare the time complexity of different tree balancing techniques
A: Common approaches:
- AVL Trees: Strict balance (height diff ≤ 1), faster lookups
- Red-Black Trees: Relaxed balance, faster insertions/deletions
- B-Trees: Optimized for disk access, good cache locality
- Splay Trees: Self-adjusting, good for temporal locality

## 6. Distributed Data Structures
Q: How would you implement a distributed cache with eventual consistency?
A: Key considerations:
- Consistent hashing for node distribution
- Vector clocks for conflict resolution
- Gossip protocol for membership
- Anti-entropy for synchronization
- Merkle trees for efficient consistency checking

## 7. Streaming Algorithms
Q: How would you count unique elements in a large data stream?
A: Techniques include:
- HyperLogLog for approximate counting
- Count-Min Sketch for frequency estimation
- Bloom filters for membership testing
- Reservoir sampling for random sampling
- Sliding window algorithms

## 8. Advanced Python-Specific
Q: How would you implement a custom iterator that's memory efficient?
A: Best practices:
- Use generators instead of storing all data
- Implement __iter__ and __next__ methods
- Consider making it a context manager if needed (to properly manage resources and prevent memory leaks)
- Use itertools for composition
- Implement __length_hint__ for optimization:
  ```python
  class EfficientIterator:
      def __length_hint__(self):
          # Provides an estimated length for optimization
          # Example: Iterator over a large file
          try:
              # Get file size and estimate number of lines
              return self._file.seek(0, 2) // self._avg_line_length
          except:
              return NotImplemented
  ```
  This allows Python to pre-allocate space when using the iterator in operations like list(iterator), improving performance

## 9. System Design with Data Structures
Q: Design a rate limiter using appropriate data structures
A: Possible solution:
- Sliding window counter using Redis sorted sets
- Token bucket using atomic counters
- Leaky bucket using queue
- Fixed window counter using hash table
- Distributed rate limiting using Redis

## 10. Performance Optimization
Q: How would you optimize a frequently accessed cache?
A: Strategies include:
- LRU cache using OrderedDict
- Implement generational garbage collection
- Use probabilistic data structures
- Implement write-behind caching
- Consider cache warming strategies
