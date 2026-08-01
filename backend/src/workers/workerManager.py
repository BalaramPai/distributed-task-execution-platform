# src/workers/workerManager.py

from threading import Lock
from src.workers.worker import Worker
from src.schemas.enums import WorkerState

workers = []    # Without storing the thread objects, we can't answer questions like how many workers are there, or if any worker is alive etc.
                # As if we dont then after execution of the start worker function all threads will be forgotten, so to keep a track we use the module level-list.
running_tasks = 0
running_tasks_lock = Lock()
workers_list_lock = Lock()      # So when we access or use or edit the workers list there are no race condition as it is shared by multiple workers.


def start_workers(NUM_WORKERS):
    from src.workers.taskWorker import worker   # If imported on Top there will be a circular import between taskWorker and workerManager.
    for i in range(1,NUM_WORKERS+1):
        worker_instance = Worker(i,worker)
        worker_instance.start()
        with workers_list_lock:
            workers.append(worker_instance)
            
            
def get_worker_count():
    with workers_list_lock:
        return len(workers)


def get_all_workers():
    with workers_list_lock:
        return workers.copy()   # So the caller cannot accidentally modify the internal list.


def get_worker(worker_id):
    with workers_list_lock:
        for worker in workers:
            if worker.worker_id == worker_id:
                return worker
    return None

def get_worker_count_by_state(state: WorkerState):
    with workers_list_lock:
        count = 0
        for worker in workers:
            if worker.state == state:
                count += 1
        return count


# These are fir the scheduler stats as it will give stats of all workers aggregated together.
def get_total_successful_tasks():
    with workers_list_lock:
        total = 0

        for worker in workers:
            total += worker.successful_tasks

        return total


def get_total_failed_tasks():
    with workers_list_lock:
        total = 0

        for worker in workers:
            total += worker.failed_tasks

        return total


def get_total_retried_tasks():
    with workers_list_lock:
        total = 0

        for worker in workers:
            total += worker.retried_tasks

        return total
        

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