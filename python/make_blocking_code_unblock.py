import asyncio
import time




def blocking_task(arg):
    # Simulate a blocking operation
    import time
    time.sleep(2)
    return f"Processed {arg}"

async def unblocing_sleep(arg):
    await asyncio.sleep(2)
    return f"Processed {arg}"

async def main():
    start_time = time.perf_counter()
    
    loop = asyncio.get_running_loop()
    tasks = []
    for i in range(5):
        # Offload blocking_task to a ThreadPoolExecutor
        blocking = loop.run_in_executor(None, blocking_task, i)
        # Add unblocking_sleep task
        unblocking = unblocing_sleep(i)
        tasks.append(blocking)
        tasks.append(unblocking)
    results = await asyncio.gather(*tasks)
    print(results)
    
    end_time = time.perf_counter()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

asyncio.run(main())
