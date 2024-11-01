"""
Threading vs Asyncio in Python

Key Differences:
1. Concurrency Model
   - Threading: Preemptive multitasking, OS decides when to switch threads
   - Asyncio: Cooperative multitasking, tasks explicitly yield control

2. Use Cases
   - Threading: Best for I/O-bound tasks with blocking operations
     Example: Reading large files from disk
     ```python
     def read_file(filename):
         with open(filename, 'r') as f:
             return f.read()  # Blocking I/O operation
     
     # Using threads for parallel file reading
     threads = [
         threading.Thread(target=read_file, args=(f'file{i}.txt',))
         for i in range(3)
     ]
     ```

   - Asyncio: Best for I/O-bound tasks that can be made non-blocking
     Example: Making HTTP requests
     ```python
     async def fetch_url(url):
         async with aiohttp.ClientSession() as session:
             async with session.get(url) as response:
                 return await response.text()  # Non-blocking I/O
     
     # Using asyncio for concurrent HTTP requests
     urls = ['http://example.com', 'http://example.org']
     tasks = [fetch_url(url) for url in urls]
     results = await asyncio.gather(*tasks)
     ```

3. State Management
   - Threading: Shared memory, need locks/synchronization even with GIL (GIL only ensures atomic bytecode operations, not atomic operations across multiple lines)
   Example: in lock-examples.py

   - Asyncio: Single thread, no need for locks

Examples demonstrating when to use each:
"""

# Threading Example - Good for blocking I/O operations
import threading
import time

def blocking_io():
    # Simulating blocking I/O operation (e.g. reading from slow disk)
    time.sleep(1)
    return "data"

def thread_example():
    threads = []
    for i in range(3):
        thread = threading.Thread(target=blocking_io)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

# Asyncio Example - Good for network operations
import asyncio

async def non_blocking_io():
    # Simulating non-blocking I/O (e.g. network request)
    await asyncio.sleep(1)
    return "data"

async def asyncio_example():
    # Creates multiple coroutines and runs them concurrently
    tasks = [non_blocking_io() for _ in range(3)]
    await asyncio.gather(*tasks)

"""
When to Choose Threading:
- CPU-bound tasks that release the GIL (e.g. numpy operations)
- Working with blocking I/O that can't be made async
- Integration with blocking libraries
- Simple parallel tasks where performance isn't critical

When to Choose Asyncio:
- Network I/O operations (web requests, API calls)
- High number of concurrent connections
- When you need fine-grained control over concurrency
- Modern async libraries available for your use case
"""

if __name__ == "__main__":
    # Run threading example
    print("Running threading example...")
    start = time.time()
    thread_example()
    print(f"Threading took: {time.time() - start:.2f} seconds")

    # Run asyncio example
    print("\nRunning asyncio example...")
    start = time.time()
    asyncio.run(asyncio_example())
    print(f"Asyncio took: {time.time() - start:.2f} seconds")
