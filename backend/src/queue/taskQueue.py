# src/queue/taskQueue.py
import heapq    
from threading import Lock

from src.queue.utils.priority import PRIORITY_MAP,REVERSE_PRIORITY_MAP
from src.schemas.enums import TaskPriority


class TaskQueue:

    def __init__(self):
        self.task_queue = []             # Reason we use a list is cause heapq inbuilt works on a list there is no class as such like how we had for deque and hence needed and object creation and stuff.
        self.sequence = 0                # so we have this cause when the priorities are same then we need to keep a track of the sequence in which they arrived so we can do FIFO.
        self.lock = Lock()               # We use the locking for "Thread-safe TaskQueue" , Synchronisation, Mutual Exclusion.


    def enqueue(self, task_id: int, priority: TaskPriority):
        with self.lock:                  # So the "with lock:" statement internally acquires and released the lock before and after the process.
            priority_value = PRIORITY_MAP[priority]
            self.sequence += 1

            heapq.heappush(self.task_queue,(priority_value, self.sequence, task_id))    # Here we compare the priority first if tied then sequence.
            return True

    def dequeue(self):
        with self.lock:
            if self.task_queue:
                _, _, task_id = heapq.heappop(self.task_queue)  # Here as we only need the task_id we can ignore the priority and sequence which has been unpacked in the pop operation.
                return task_id
        return None

    def peek(self):
        with self.lock:
            if self.task_queue:
                _, _, task_id = self.task_queue[0]      # again here of the top most element we only need the task_id when unpacked from the heap.
                return task_id
        return None

    def size(self):
        with self.lock:
            return len(self.task_queue)

    def is_empty(self):
        return self.size() == 0
    
    def get_queue_snapshot(self):
        task_list = []
        with self.lock:
            for priority, sequence, task_id in self.task_queue:
                task_list.append({
                                    "task_id": task_id,
                                    "priority": REVERSE_PRIORITY_MAP[priority]
                                })
        return task_list