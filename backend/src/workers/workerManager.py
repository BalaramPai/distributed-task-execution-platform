# src/workers/workerManager.py

import threading
from src.workers.taskWorker import worker

workers = []    # Without storing the thread objects, we can't answer questions like how many workers are there, or if any worker is alive etc.
                # As if we dont then after execution of the start worker function all threads will be forgotten, so to keep a track we use the module level-list.

def start_workers(NUM_WORKERS):
    for i in range(1,NUM_WORKERS+1):
            worker_thread = threading.Thread(target=worker,daemon=True,name=f"Worker-{i}")
            worker_thread.start()
            workers.append(worker_thread)