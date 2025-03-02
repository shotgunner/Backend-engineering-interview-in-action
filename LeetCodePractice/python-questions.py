# Senior Python Developer Interview Questions with Solutions

# 1. Implement a decorator that measures function execution time
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds to execute")
        return result
    return wrapper

@measure_time
def slow_function():
    time.sleep(1)
    return "Done!"

# 2. Implement a custom context manager for file handling
class FileHandler:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
        
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# 3. Implement a thread-safe singleton pattern
from threading import Lock

class Singleton:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

# 4. Implement a custom iterator for Fibonacci sequence
class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.prev = 0
        self.curr = 1
        self.count = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration
        
        result = self.prev
        self.prev, self.curr = self.curr, self.prev + self.curr
        self.count += 1
        return result

# 5. Implement LRU Cache using OrderedDict
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
        
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
        
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Example usage:
if __name__ == "__main__":
    # Test decorator
    print("\nTesting time decorator:")
    slow_function()
    
    # Test context manager
    print("\nTesting context manager:")
    with FileHandler("test.txt", "w") as f:
        f.write("Hello, World!")
    
    # Test singleton
    print("\nTesting singleton:")
    s1 = Singleton()
    s2 = Singleton()
    print(f"Are instances same? {s1 is s2}")
    
    # Test Fibonacci iterator
    print("\nTesting Fibonacci iterator:")
    fib = Fibonacci(5)
    print(list(fib))  # [0, 1, 1, 2, 3]
    
    # Test LRU Cache
    print("\nTesting LRU Cache:")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))       # returns 1
    cache.put(3, 3)          # evicts key 2
    print(cache.get(2))       # returns -1 (not found)
