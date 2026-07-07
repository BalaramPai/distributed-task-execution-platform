# src/workers/taskWorker.py
from src.queue.queueManager import task_queue
from src.dao.taskDao import get_task_for_worker
from src.database.database import SessionLocal
from time import sleep

db = SessionLocal()

try:
    while True:
        if task_queue.is_empty():
            sleep(1)
            continue
            
        task_id = task_queue.dequeue()
        if task_id:
            print("The folowing task has been pushed forward for processing..")
            print(get_task_for_worker(db,task_id))
finally:
    db.close()
        
        
        
            
        