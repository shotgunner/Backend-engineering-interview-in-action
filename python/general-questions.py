# Technical Interview Questions and Answers
# Based on format from learnxinyminutes.com

"""
Let's explore common technical interview questions and detailed answers
organized by topic areas.

We'll use a Q&A format with practical examples and code snippets.
"""

########################
### Data Structures ###
########################

# Q: How would you implement a basic binary search tree in Python?
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None 
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

# Q: What's the time complexity for BST operations?
"""
A: For a balanced BST:
- Search: O(log n)
- Insert: O(log n) 
- Delete: O(log n)

For unbalanced BST (worst case):
- All operations become O(n)
"""

#############################
### Operating Systems ###
#############################

# Q: How do you implement a basic producer-consumer pattern?
from threading import Thread, Lock
from queue import Queue
import time

def producer_consumer_example():
    queue = Queue(maxsize=10)
    
    def producer():
        for i in range(5):
            queue.put(i)
            print(f"Produced: {i}")
            time.sleep(1)
    
    def consumer():
        while True:
            item = queue.get()
            print(f"Consumed: {item}")
            queue.task_done()
    
    # Start threads
    Thread(target=producer).start()
    Thread(target=consumer).start()

#########################
### Networking ###
#########################

# Q: How would you implement a basic TCP server?
import socket

def basic_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(5)
    
    while True:
        client, addr = server.accept()
        data = client.recv(1024)
        client.send(b"Message received")
        client.close()

########################
### Databases ###
########################

# Q: How do you handle database transactions in Python?
"""
A: Using SQLAlchemy as an example:
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def transaction_example():
    engine = create_engine('postgresql://user:pass@localhost/db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Perform database operations
        session.add(some_object)
        session.add(another_object)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

#########################
### Web Development ###
#########################

# Q: How would you implement basic rate limiting?
from time import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def is_allowed(self):
        now = time()
        
        # Remove old requests
        while self.requests and self.requests[0] <= now - self.time_window:
            self.requests.popleft()
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

#########################
### System Design ###
#########################

# Q: How would you design a basic cache with expiration?
from collections import OrderedDict
from time import time

class TimedCache:
    def __init__(self, expiration_seconds):
        self.expiration = expiration_seconds
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time() - timestamp < self.expiration:
                return value
            else:
                del self.cache[key]
        return None
    
    def put(self, key, value):
        self.cache[key] = (value, time())
        # Cleanup expired entries
        self._cleanup()
    
    def _cleanup(self):
        now = time()
        for key, (_, timestamp) in list(self.cache.items()):
            if now - timestamp >= self.expiration:
                del self.cache[key]

"""
These examples demonstrate fundamental concepts often discussed in 
technical interviews. Each implementation shows practical usage
and common patterns you might encounter in real-world scenarios.

Remember to discuss:
- Trade-offs in your design choices
- Scalability considerations
- Error handling
- Testing strategies
- Performance implications
"""

if __name__ == "__main__":
    # Example usage of TimedCache
    cache = TimedCache(expiration_seconds=5)
    cache.put("key1", "value1")
    print(cache.get("key1"))  # Returns "value1"
    time.sleep(6)
    print(cache.get("key1"))  # Returns None

