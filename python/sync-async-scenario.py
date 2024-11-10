# suppose this scenario. suppose this piece of code:


# You have a requirement that you have to download a lot of data from a sync library
# without using any external dependencies except Python, with an async websocket, 
# considering that the client connects to it, and you have to update the websocket client as well.
# What percentage of downloads are done on the web socket.
# Let's assume that the sync library you are using to download data has a hook that you give a callable to and it calls every n percent of the download. Such an interface:


# def download_hook(info): 
#    ...
#    # notify your webhook client which is async
# download_big_data(hook=download_hook, every_n_percent=10)   => this is a sync function

# Actually, the challenge of this question is that the sync and async code talk to each other in real time in a process.
# First question: How do you implement this?
# Second question: If there was no requirement for foreign dependency, what would you use? and why?
# ================================================================================================

# Here's how to handle sync/async communication for download progress updates via websocket:

import asyncio
import queue
import threading
from asyncio import Queue
from typing import Callable

# Shared queue between sync and async code
progress_queue = queue.Queue()

# Async websocket handler
async def websocket_handler(websocket):
    while True:
        try:
            # Get progress updates from the queue
            progress = await asyncio.get_event_loop().run_in_executor(
                None, progress_queue.get
            )
            # Send progress to websocket client
            await websocket.send(str(progress))
        except Exception:
            break

# Sync download hook
def download_hook(progress: int):
    # Put progress in queue for async code to consume
    progress_queue.put(progress)

def download_in_thread(hook: Callable):
    # Run sync download in separate thread
    def _download():
        download_big_data(hook=hook, every_n_percent=10)
    
    thread = threading.Thread(target=_download)
    thread.start()

# Answer to second question:
"""
If external dependencies were allowed, I would use:

1. aiohttp - For async websocket server implementation
2. asyncio-queue - For better sync/async queue communication
3. FastAPI - For easier async web framework integration

Benefits:
- aiohttp provides robust websocket implementation
- asyncio-queue handles backpressure better
- FastAPI simplifies async endpoint creation and websocket handling
- All are well-tested in production environments

The current solution using basic Python is more complex and potentially less reliable,
but works when external dependencies aren't allowed.
"""

