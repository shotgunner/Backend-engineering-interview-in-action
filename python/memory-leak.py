
import time
from typing import List

def memory_leak_example():
    """
    This function demonstrates a memory leak by storing references 
    that are never cleaned up
    """
    leaked_data = []
    
    while True:
        # Creating new objects and storing references that are never removed
        # This is a memory leak because the list keeps growing without bounds
        leaked_data.append("*" * 10000000)  # Each string is ~1MB
        time.sleep(0.1)
        print(f"Current list size: {len(leaked_data)}")
        # The leaked_data list is never cleared and keeps consuming more memory

def high_memory_usage_example():
    """
    This function demonstrates legitimate high memory usage
    with proper cleanup
    """
    while True:
        # Creating large data structure that gets properly cleaned up
        large_data = ["*" * 10000000 for _ in range(100)]  # Create ~100MB array
        
        # Process the data
        result = sum(len(x) for x in large_data)
        print(f"Processed {result} characters")
        
        # large_data goes out of scope here and can be garbage collected
        # Memory is properly released after each iteration
        time.sleep(0.1)

# Example usage:
if __name__ == "__main__":
    print("Running memory leak example (Ctrl+C to stop)...")
    try:
        # WARNING: This will eventually crash due to memory leak
        memory_leak_example()
    except KeyboardInterrupt:
        print("\nStopped memory leak example")
    
    print("\nRunning high memory usage example (Ctrl+C to stop)...")
    try:
        # This will use lots of memory but won't leak
        high_memory_usage_example()
    except KeyboardInterrupt:
        print("\nStopped high memory usage example")



def prevent_memory_leak_example():
    """
    This function demonstrates best practices to prevent memory leaks
    """
    # 1. Use context managers (with statements) for proper cleanup
    with open("large_file.txt", "w") as f:
        f.write("Some data")  # File handle automatically closed
    
    # 2. Use weak references when needed
    import weakref
    class Cache:
        def __init__(self):
            # Use WeakKeyDictionary instead of regular dict
            self.data = weakref.WeakKeyDictionary()
    
    # 3. Explicitly delete large objects when done
    large_data = ["*" * 1000000 for _ in range(10)]
    # Process data...
    del large_data
    
    # 4. Use generators for large datasets instead of lists
    def process_large_dataset():
        for i in range(1000000):
            yield i * i
            
    # Memory efficient - only one number at a time
    for num in process_large_dataset():
        print(num)
        
    # 5. Clear collections explicitly when needed
    data_list = []
    try:
        for _ in range(1000):
            data_list.append("*" * 100000)
            # Process data...
    finally:
        data_list.clear()  # Explicitly clear the list
    
    # 6. Use slots to reduce memory for many instances
    class MemoryEfficientClass:
        __slots__ = ['name', 'value']
        def __init__(self, name, value):
            self.name = name
            self.value = value

if __name__ == "__main__":
    print("\nRunning memory leak prevention example...")
    try:
        prevent_memory_leak_example()
        print("Successfully demonstrated memory leak prevention techniques")
    except Exception as e:
        print(f"An error occurred: {e}")


