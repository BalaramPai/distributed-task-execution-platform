# src/queue/taskQueue.py
from collections import deque
from threading import Lock


class TaskQueue:
    def __init__(self):
        self.task_queue = deque()
        self.lock = Lock()                      # We use the locking for "Thread-safe TaskQueue" , Synchronisation, Mutual Exclusion.

    def enqueue(self,task_id):
        with self.lock:                         # So the "with lock:" statement internally acquires and released the lock before and after the process.
            self.task_queue.append(task_id)
            return True
    
    def dequeue(self):
        with self.lock:                         # Here also the lock is acquired and released irrespectove of an error or not.
            if self.task_queue:
                return self.task_queue.popleft()
        return None
        
    def peek(self):
        with self.lock:
            if not self.is_empty():
                return self.task_queue[0]
        return None
        
    def size(self):
        return len(self.task_queue)
            
    def is_empty(self):
        return self.size() == 0

       

    