# src/queue/taskQueue.py
import heapq    
from threading import Lock
from datetime import datetime

from src.queue.utils.priority import PRIORITY_MAP
from src.schemas.enums import TaskPriority
from src.queue.queueEntry import QueueEntry

from src.constants.schedulerConstants import AGING_RULES, THRESHOLD, PROMOTE_TO

class TaskQueue:

    def __init__(self):
        self.task_queue = []             # Reason we use a list is cause heapq inbuilt works on a list there is no class as such like how we had for deque and hence needed and object creation and stuff.
        self.sequence = 0                # so we have this cause when the priorities are same then we need to keep a track of the sequence in which they arrived so we can do FIFO.
        self.lock = Lock()               # We use the locking for "Thread-safe TaskQueue" , Synchronisation, Mutual Exclusion.


    def enqueue(self, task_id: int, priority: TaskPriority):
        with self.lock:                  # So the "with lock:" statement internally acquires and released the lock before and after the process.
            
            # We have created a QueueEntry class which holds all the runtime data about the task for the scheduler and within the scheduler as meta-data.
            # We have replaced task_id with entry where itll hold all values of the task such as id,effective,original, time created(done by default).
            entry = QueueEntry(                     
                                task_id=task_id,
                                original_priority=priority,
                                effective_priority=priority,
                              )
            
            priority_value = PRIORITY_MAP[entry.effective_priority] # As the task ages the priority changes and that value is held in the effective_prioroty variable and the start value is original priority so there is no inconsistency of data.

            heapq.heappush(self.task_queue,(priority_value, self.sequence, entry))    # Here we compare the priority first if tied then sequence.
            self.sequence += 1   # We increase the sequence after the insertion as incase any error is thrown by push then there will be an invalid increase in sequence.

            return True

    def dequeue(self):
        with self.lock:
            if self.task_queue:
                _, _, entry = heapq.heappop(self.task_queue)  # Here as we only need the task_id we can ignore the priority and sequence which has been unpacked in the pop operation.
                return entry.task_id
        return None

    def peek(self):
        with self.lock:
            if self.task_queue:
                _, _, entry = self.task_queue[0]      # again here of the top most element we only need the task_id when unpacked from the heap.
                return entry.task_id
        return None

    def size(self):
        with self.lock:
            return len(self.task_queue)

    def is_empty(self):
        return self.size() == 0
    
    def get_queue_snapshot(self):
        task_list = []
        with self.lock:
            for _, _ , entry in self.task_queue:
                task_list.append({
                                    "task_id": entry.task_id,
                                    "priority": entry.effective_priority.value
                                })
        return task_list
    
    def apply_aging(self):
        """
        Checks every queued task and promotes tasks that have
        waited longer than the configured aging threshold.

        After promotion, rebuilds the heap so the new priorities
        are reflected in scheduling.
        """
        with self.lock:
            priority_updated = False
            
            for _, _, entry in self.task_queue:
                waiting_time = entry.get_waiting_time()
                rule = AGING_RULES[entry.effective_priority]

                if (
                    rule[THRESHOLD] is not None
                    and waiting_time >= rule[THRESHOLD]
                ):
                    entry.effective_priority = rule[PROMOTE_TO]
                    entry.last_priority_update_at = datetime.utcnow()
                    priority_updated = True

            # Once we have got the new status we also have to update the tasks effective_piority in the heap, the below code does that.
            if priority_updated:
                self.task_queue = [
                    (
                        PRIORITY_MAP[entry.effective_priority],
                        sequence,
                        entry,
                    )
                    for _, sequence, entry in self.task_queue
                ]

                heapq.heapify(self.task_queue)