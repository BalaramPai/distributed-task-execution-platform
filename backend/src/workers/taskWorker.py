# src/workers/taskWorker.py
from src.queue.queueManager import task_queue
from src.database.database import SessionLocal
from src.service.taskService import process_task

import threading
from time import sleep


def worker():
    db = SessionLocal()
    try:
        while True:
            task_id = task_queue.dequeue()
            if task_id is None:         # Instead of is_empty as it can incurr Time-of-Check to Time-of-Use (TOCTOU) race condition.
                sleep(1)
                continue
            
            else:
                print(f"{threading.current_thread().name} picked Task {task_id}")
                process_task(db, task_id)               
    finally:
        db.close()
        
        
                
        
        
        
            
    
          