import asyncio
import aiohttp
import time
from typing import List, Dict
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

# Example data class for API responses
@dataclass
class TravelDestination:
    name: str
    weather: str
    population: int

# Simulating I/O-bound operations (e.g., API calls)
async def fetch_destination_data(destination: str) -> Dict:
    """Simulate API call to fetch destination data"""
    async with aiohttp.ClientSession() as session:
        # Simulating different API endpoints
        endpoints = [
            f"http://api.example.com/weather/{destination}",
            f"http://api.example.com/population/{destination}"
        ]
        
        async def fetch_url(url: str) -> Dict:
            # Simulate network delay
            await asyncio.sleep(1)
            return {"data": f"Response from {url}"}
        
        # Gather multiple API calls
        tasks = [fetch_url(url) for url in endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "name": destination,
            "weather": "sunny",  # Simulated data
            "population": 1000000  # Simulated data
        }

# CPU-bound task example
def cpu_intensive_task(numbers: List[int]) -> int:
    """Simulate CPU-intensive calculation"""
    return sum(n * n for n in numbers)

# Combining CPU-bound and I/O-bound operations
async def process_destination(destination: str) -> TravelDestination:
    # I/O-bound operation
    data = await fetch_destination_data(destination)
    
    # CPU-bound operation in thread pool
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        # Simulate some CPU-intensive data processing
        result = await loop.run_in_executor(
            pool, 
            cpu_intensive_task, 
            [1, 2, 3, 4, 5]
        )
    
    return TravelDestination(
        name=data["name"],
        weather=data["weather"],
        population=data["population"]
    )

# Example of handling timeouts
async def fetch_with_timeout(destination: str, timeout: float = 2.0) -> Dict:
    try:
        async with asyncio.timeout(timeout):
            return await fetch_destination_data(destination)
    except asyncio.TimeoutError:
        return {"error": f"Timeout fetching data for {destination}"}

# Example of concurrent tasks with rate limiting
async def process_destinations_with_semaphore(
    destinations: List[str], 
    concurrency_limit: int = 3
) -> List[TravelDestination]:
    semaphore = asyncio.Semaphore(concurrency_limit)
    
    async def fetch_with_semaphore(dest: str) -> TravelDestination:
        async with semaphore:
            return await process_destination(dest)
    
    tasks = [fetch_with_semaphore(dest) for dest in destinations]
    return await asyncio.gather(*tasks)

# Example of handling cancellation
async def cancellable_task():
    try:
        while True:
            await asyncio.sleep(1)
            print("Task is running...")
    except asyncio.CancelledError:
        print("Task was cancelled!")
        # Cleanup code here
        raise  # Re-raise to properly propagate cancellation

async def main():
    # Example 1: Basic concurrent execution
    destinations = ["Amsterdam", "Paris", "Tokyo"]
    results = await asyncio.gather(
        *[process_destination(dest) for dest in destinations]
    )
    print("Processed destinations:", [r.name for r in results])
    
    # Example 2: Timeout handling
    result = await fetch_with_timeout("London", timeout=1.5)
    print("Timeout example:", result)
    
    # Example 3: Rate-limited concurrent execution
    rate_limited_results = await process_destinations_with_semaphore(
        ["Rome", "Berlin", "Madrid", "Vienna"], 
        concurrency_limit=2
    )
    print("Rate-limited results:", [r.name for r in rate_limited_results])
    
    # Example 4: Task cancellation
    task = asyncio.create_task(cancellable_task())
    await asyncio.sleep(2)  # Let it run for 2 seconds
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Main: task cancellation handled")

if __name__ == "__main__":
    # Run the async program
    start_time = time.time()
    asyncio.run(main())
    print(f"Total execution time: {time.time() - start_time:.2f} seconds") 