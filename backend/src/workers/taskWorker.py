# src/workers/taskWorker.py
from src.queue.queueManager import task_queue
from src.database.database import SessionLocal
from src.service.taskService import execute_task
from time import sleep


db = SessionLocal()

def worker():
    try:
        while True:
            if task_queue.is_empty():
                sleep(1)
                continue
                
            task_id = task_queue.dequeue()
            
            if task_id:
                print(f"Worker picked Task {id}")
                execute_task(db,task_id)
                
    finally:
        db.close()
        
        
        
            
    
          