# src/workers/taskWorker.py
from src.queue.queueManager import task_queue
from src.database.database import SessionLocal
from src.service.taskService import process_task
from src.workers.workerManager import increment_running_tasks,decrement_running_tasks

import threading
from time import sleep


# We are passing the worker object in worker so we can get the metadata and details of the current worker or the worker that is working.
def worker(current_worker):   
    db = SessionLocal()
    try:
        while True:
            
            # Before any task is processed by the worker we apply aging and to the tasks and update the heap tasks with their new priorities.
            task_queue.apply_aging()
            
            task_id = task_queue.dequeue()  # Used so while the task queue is empty it keeps refreshing.
            if task_id is None:         # Instead of is_empty as it can incurr Time-of-Check to Time-of-Use (TOCTOU) race condition.
                sleep(1)
                continue
            
            else:
                increment_running_tasks()
                current_worker.current_task = task_id  # The worker has picked this task.
                try:
                    print(f"{threading.current_thread().name} picked Task {task_id}")
                    process_task(db, task_id)
                finally:                            # We used finally as even if the task fails, the scheduler metrics remain accurate.
                    current_worker.current_task = None  # Once processed it has the worker has no task.
                    decrement_running_tasks()             
    finally:
        db.close()
        
        
                
        
        
        
            
    