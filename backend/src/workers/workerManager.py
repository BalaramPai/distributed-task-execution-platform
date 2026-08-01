# src/workers/workerManager.py

from threading import Lock
from src.workers.worker import Worker

workers = []    # Without storing the thread objects, we can't answer questions like how many workers are there, or if any worker is alive etc.
                # As if we dont then after execution of the start worker function all threads will be forgotten, so to keep a track we use the module level-list.
running_tasks = 0
running_tasks_lock = Lock()


def start_workers(NUM_WORKERS):
    from src.workers.taskWorker import worker   # If imported on Top there will be a circular import between taskWorker and workerManager.
    for i in range(1,NUM_WORKERS+1):
        worker_instance = Worker(i,worker)
        worker_instance.start()
        workers.append(worker_instance)
            
            
def get_worker_count():
    return len(workers)


def increment_running_tasks():
    global running_tasks   # Since we are modifying the module-level variable, Python needs to be explicitly told not to create a new local variable.

    with running_tasks_lock:   # Protect the shared counter so multiple worker threads cannot update it simultaneously.
        running_tasks += 1     # Increment when a worker starts processing a task.


def decrement_running_tasks():
    global running_tasks   # Again, we modify the module-level variable, so 'global' is required.

    with running_tasks_lock:   # Ensure only one thread updates the counter at a time.
        running_tasks -= 1     # Decrement when a worker finishes processing, regardless of success or failure.


def get_running_tasks():
    with running_tasks_lock:   # Lock while reading so the returned value is consistent with concurrent updates.
        return running_tasks   # Only reading the variable, so 'global' is not required.