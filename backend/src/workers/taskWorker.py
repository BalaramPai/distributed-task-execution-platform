# src/workers/taskWorker.py
from src.queue.queueManager import task_queue
from src.database.database import SessionLocal
from src.service.taskService import process_task
from src.workers.workerManager import increment_running_tasks,decrement_running_tasks

import threading
from time import sleep


def worker():   
    db = SessionLocal()
    try:
        while True:
            task_id = task_queue.dequeue()  # Used so while the task queue is empty it keeps refreshing.
            if task_id is None:         # Instead of is_empty as it can incurr Time-of-Check to Time-of-Use (TOCTOU) race condition.
                sleep(1)
                continue
            
            else:
                increment_running_tasks()
                try:
                    print(f"{threading.current_thread().name} picked Task {task_id}")
                    process_task(db, task_id)
                finally:                            # We used finally as even if the task fails, the scheduler metrics remain accurate.
                    decrement_running_tasks()             
    finally:
        db.close()
        
        
                
        
        
        
            
    
          