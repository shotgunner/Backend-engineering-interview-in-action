import time
import threading
import multiprocessing
import concurrent.futures

def io_task(seconds):
    """Simulates IO-bound task by sleeping"""
    time.sleep(seconds)
    return seconds

def cpu_task(n):
    """Simulates CPU-bound task by doing calculations"""
    result = 0
    for i in range(n * 1000000):
        result += i * i
    return result

def run_sequential(tasks, task_func):
    start = time.time()
    results = []
    for task in tasks:
        results.append(task_func(task))
    end = time.time()
    return end - start

def run_threads(tasks, task_func):
    start = time.time()
    threads = []
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(task_func, tasks))
    
    end = time.time()
    return end - start

def run_processes(tasks, task_func):
    start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(task_func, tasks))
    
    end = time.time()
    return end - start

if __name__ == "__main__":
    # IO-bound tasks
    io_tasks = [0.5] * 12  # 12 tasks that each sleep for 0.5 seconds
    
    print("Running IO-bound tasks:")
    print("\nRunning sequential...")
    sequential_time = run_sequential(io_tasks, io_task)
    print(f"Sequential time: {sequential_time:.2f} seconds")
    
    print("\nRunning with threads...")
    threaded_time = run_threads(io_tasks, io_task)
    print(f"Threaded time: {threaded_time:.2f} seconds")
    
    print("\nRunning with processes...")
    process_time = run_processes(io_tasks, io_task)
    print(f"Process time: {process_time:.2f} seconds")
    
    print("\nIO-bound Results comparison:")
    print(f"Sequential vs Threaded speedup: {sequential_time/threaded_time:.2f}x")
    print(f"Sequential vs Process speedup: {sequential_time/process_time:.2f}x")
    print(f"Threaded vs Process speedup: {threaded_time/process_time:.2f}x")

    # CPU-bound tasks
    cpu_tasks = [50] * 12  # 12 CPU-intensive tasks
    
    print("\n\nRunning CPU-bound tasks:")
    print("\nRunning sequential...")
    sequential_time = run_sequential(cpu_tasks, cpu_task)
    print(f"Sequential time: {sequential_time:.2f} seconds")
    
    print("\nRunning with threads...")
    threaded_time = run_threads(cpu_tasks, cpu_task)
    print(f"Threaded time: {threaded_time:.2f} seconds")
    
    print("\nRunning with processes...")
    process_time = run_processes(cpu_tasks, cpu_task)
    print(f"Process time: {process_time:.2f} seconds")
    
    print("\nCPU-bound Results comparison:")
    print(f"Sequential vs Threaded speedup: {sequential_time/threaded_time:.2f}x")
    print(f"Sequential vs Process speedup: {sequential_time/process_time:.2f}x")
    print(f"Threaded vs Process speedup: {threaded_time/process_time:.2f}x")
