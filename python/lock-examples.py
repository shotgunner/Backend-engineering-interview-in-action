import threading
import time

counter = 0
def increment_counter():
    global counter
    for _ in range(100):
        current = counter  # Read
        time.sleep(0.001) # Context switch possible here
        counter = current + 1  # Write based on stale value

threads = []
for _ in range(2):
    t = threading.Thread(target=increment_counter)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Without lock final counter: {counter}")  # Will be less than 200

# With lock - guarantees correct results 
counter = 0
lock = threading.Lock()
def safe_increment():
    global counter
    for _ in range(100):
        with lock:
            current = counter
            time.sleep(0.001)
            counter = current + 1

threads = []
for _ in range(2):
    t = threading.Thread(target=safe_increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print(f"With lock final counter: {counter}")  # Always prints 200


# With asyncio - demonstrating race condition without lock
import asyncio

counter = 0

async def async_increment():
    global counter
    for _ in range(100):
        current = counter
        await asyncio.sleep(0.001)  # Non-blocking sleep
        counter = current + 1

async def main():
    global counter
    counter = 0
    tasks = []
    for _ in range(2):
        tasks.append(asyncio.create_task(async_increment()))
    await asyncio.gather(*tasks)
    print(f"Without lock final counter: {counter}")  # Will be less than 200 due to race condition

# Run the async example
asyncio.run(main())
