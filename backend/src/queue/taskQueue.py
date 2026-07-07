# src/queue/taskQueue.py
from collections import deque

class TaskQueue:
    def __init__(self):
        self.task_queue = deque()

    def enqueue(self,task_id):
        self.task_queue.append(task_id)
        return True
    
    def dequeue(self):
        if self.task_queue:
            return self.task_queue.popleft()
        return None
        
    def peek(self):
        if not self.is_empty():
            return self.task_queue[0]
        return None
        
    def size(self):
        return len(self.task_queue)
            
    def is_empty(self):
        return self.size() == 0

       

    