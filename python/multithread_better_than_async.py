import time
import asyncio
import requests

urls = [
    'https://www.example.com',
    'https://www.python.org',
    'https://www.openai.com',
    # Add more URLs as needed
]

def fetch_url(url):
    response = requests.get(url)
    print(f"Fetched {url} with status {response.status_code}")

async def main():
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, fetch_url, url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"`asyncio` with run_in_executor took {end_time - start_time:.2f} seconds")
