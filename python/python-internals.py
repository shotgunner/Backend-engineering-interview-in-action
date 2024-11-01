"""
Senior Python Developer Interview Questions About Python Internals
"""

import sys

# Q1: Explain Python's memory management and garbage collection
def memory_management_example():
    # Python uses reference counting as primary mechanism
    x = []
    print(f"Reference count: {sys.getrefcount(x)}")  # 2 (1 + getrefcount itself)
    
    y = x  # Increases ref count
    print(f"Reference count after assignment: {sys.getrefcount(x)}")  # 3
    
    # Circular references are handled by generational garbage collector
    class Node:
        def __init__(self):
            self.next = None
            
    a = Node()
    b = Node()
    a.next = b
    b.next = a
    print(f"Reference count after circular reference: {sys.getrefcount(a)}")  # 2
    print(f"Reference count after circular reference: {sys.getrefcount(b)}")  # 2
    # Without GC, these circular refs would never be cleaned up
    
# Example demonstrating why GIL exists and its relation to garbage collection
def gil_and_gc_example():
    # The GIL is necessary because Python's memory management is not thread-safe
    # Here's an example showing reference counting in action
    
    shared_list = []
    ref_count = sys.getrefcount(shared_list)
    print(f"Initial reference count: {ref_count}")
    
    def manipulate_data():
        nonlocal shared_list
        # Without GIL, these operations could cause race conditions
        # between reference counting and garbage collection
        for _ in range(1000):
            shared_list.append("some data")
            shared_list.pop()
            
    # Create threads that would potentially conflict without GIL
    import threading
    thread1 = threading.Thread(target=manipulate_data)
    thread2 = threading.Thread(target=manipulate_data)
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    
    # Reference count remains accurate because GIL prevented race conditions
    final_ref_count = sys.getrefcount(shared_list)
    print(f"Final reference count: {final_ref_count}")
    print("Without GIL, reference counting would be unreliable")
    print("and memory leaks or crashes could occur")

gil_and_gc_example()





# Q2: What is the Global Interpreter Lock (GIL)?
"""
The GIL is a mutex that protects access to Python objects, preventing multiple 
threads from executing Python bytecode at once. This is why Python threads 
can't run in parallel on multiple CPU cores.

Key points:
- Only affects CPython implementation
- One thread can execute Python code at a time
- Released during I/O operations
- Doesn't impact multiprocessing
"""

# Q3: How does Python's import system work?
"""
1. sys.modules cache check
2. Find module spec (finder)
3. Load module (loader)
4. Create module object
5. Execute module code
6. Cache module

Import hooks allow customizing this process.
"""

def custom_import_example():
    import sys
    class CustomImporter:
        def find_spec(self, fullname, path, target=None):
            print(f"Attempting to import: {fullname}")
            return None
            
    sys.meta_path.insert(0, CustomImporter())

# Q4: Explain Python's descriptor protocol
class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = self.function(obj)
        setattr(obj, self.name, value)
        return value

class Example:
    @LazyProperty
    def expensive_computation(self):
        print("Computing...")
        return sum(range(1000000))

# Q5: How does Python handle method resolution order (MRO)?
"""
Python uses C3 linearization algorithm for MRO.
Key points:
- Determines order of method lookup in inheritance
- Ensures consistent class hierarchy
- Can be viewed using Class.__mro__
"""

class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(f"MRO for class D: {D.__mro__}")

# Q6: Explain metaclasses and their use cases
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

# Q7: How does Python's async/await work internally?
"""
- Based on coroutines and event loop
- Uses generator-based coroutines under the hood
- Event loop manages scheduling of coroutines
- async def creates coroutine function
- await suspends execution until coroutine completes
"""

async def coroutine_example():
    async def nested():
        return 42
    result = await nested()
    return result

# Q8: Explain Python's context manager protocol
class CustomContextManager:
    def __init__(self, name):
        self.name = name
        
    def __enter__(self):
        print(f"Entering {self.name}")
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Exiting {self.name}")
        return False  # Don't suppress exceptions

if __name__ == "__main__":
    # Run examples as needed
    pass
