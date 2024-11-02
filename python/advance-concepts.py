"""
Advanced Python Concepts and Examples
Demonstrating senior-level Python features and best practices
"""

####################################################
## 1. Advanced Function Decorators
####################################################

from functools import wraps
import time
from typing import Any, Callable, TypeVar, ParamSpec

# Type hints for generic decorator
P = ParamSpec('P')
R = TypeVar('R')

def timing_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Measures execution time of decorated function"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

def memoize(func: Callable[P, R]) -> Callable[P, R]:
    """Caches results of expensive function calls"""
    cache = {}
    @wraps(func) 
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

####################################################
## 2. Context Managers and Descriptors
####################################################

from contextlib import contextmanager
from typing import Generator

@contextmanager
def timer() -> Generator[None, None, None]:
    """Context manager for timing code blocks"""
    # Using perf_counter() instead of time() because:
    # 1. time() can jump backwards if system clock is adjusted, while perf_counter() uses platform-specific high-resolution timers
    #    (On Linux: CLOCK_MONOTONIC, on Windows: QueryPerformanceCounter, on macOS: mach_absolute_time)
    # 2. Higher resolution - nanosecond precision
    # 3. Not affected by system clock updates
    # Perfect for performance measurements
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"Time elapsed: {end - start:.6f} seconds")

class LazyProperty:
    """Descriptor for lazy-loaded properties"""
    def __init__(self, func: Callable[[Any], Any]):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj: Any, cls: Any) -> Any:
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value

####################################################
## 3. Advanced Metaclasses
####################################################

class Singleton(type):
    """Metaclass for creating singleton classes"""
    _instances = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class RegisteredMeta(type):
    """Metaclass that maintains registry of subclasses"""
    _registry = {}
    
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        cls._registry[name] = new_cls
        return new_cls

####################################################
## 4. Advanced Iterators and Generators
####################################################

class CircularBuffer:
    """Circular buffer implementation using generators"""
    def __init__(self, size: int):
        self.size = size
        self.buffer = []
        
    def add(self, item: Any) -> None:
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(item)
    
    def __iter__(self):
        while True:
            for item in self.buffer:
                yield item

def infinite_sequence() -> Generator[int, None, None]:
    """Infinite sequence generator with memory efficiency"""
    num = 0
    while True:
        yield num
        num += 1

####################################################
## 5. Advanced Exception Handling
####################################################

class RetryException(Exception):
    """Custom exception for retry logic"""
    pass

def retry_on_exception(retries: int = 3, delay: float = 1.0) -> Callable:
    """Decorator that implements retry logic"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        raise RetryException(f"Failed after {retries} attempts") from e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

if __name__ == "__main__":
    # Example usage
    @timing_decorator
    @memoize
    def fibonacci(n: int) -> int:
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    with timer():
        result = fibonacci(35)
        print(f"Fibonacci result: {result}")
