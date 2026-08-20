# src/workers/taskWorker.py
from src.queue.queueManager import task_queue
from src.database.database import SessionLocal
from src.service.taskService import process_task
from src.workers.workerManager import (
    increment_running_tasks,
    decrement_running_tasks
)
from src.schemas.enums import (
    TaskStatus,
    WorkerState
)

import threading
from time import sleep


# We are passing the worker object in worker so we can get the metadata and details of the current worker or the worker that is working.
def worker(current_worker):   
    db = SessionLocal()
    try:
        while not current_worker.shutdown_event.is_set():  # If the shutdown_event is False as in no shutdown that means the worker can perform its designated task.
            
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
                    
                    # We set the status of the worker as we are going to process.
                    current_worker.state = WorkerState.BUSY
                    
                    # So the process_task function executes and returns the status of the processed task.
                    status = process_task(db, task_id)
                    
                    current_worker.tasks_executed += 1
                    
                    if status == TaskStatus.COMPLETED:
                        current_worker.successful_tasks += 1
                        
                    elif status == TaskStatus.FAILED:
                        current_worker.failed_tasks += 1
                        
                    elif status == TaskStatus.QUEUED:
                        current_worker.retried_tasks += 1
                    
                    else:
                        raise ValueError(f"Unexpected task status: {status}")
                    
                finally:                            # We used finally as it always exectues ,even if the task fails, the scheduler metrics remain accurate.
                    current_worker.current_task = None  # Once processed it has the worker has no task.
                    
                    if not current_worker.shutdown_event.is_set():  # We want to check if there has been any shutdown that has been intiated , if it hasnt then the worker is idle and waiting for another task to be assigned.
                        current_worker.state = WorkerState.IDLE  # The task is completed and the worker is idle again.
                        
                    decrement_running_tasks()             
    finally:
        current_worker.state = WorkerState.STOPPED  # If the shutdown has been initiated.
        db.close()
        
        
                
        
        
        
            
    