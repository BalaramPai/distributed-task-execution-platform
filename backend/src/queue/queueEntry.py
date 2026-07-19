# src/queue/queueEntry.py

from dataclasses import dataclass, field
from datetime import datetime

from src.schemas.enums import TaskPriority


"""
    Represents a single entry inside the scheduler's priority queue.

    This is NOT the database Task model.

    It only stores runtime information required by the scheduler
    while the task is waiting in the queue.

    The database remains the source of truth for the actual task.
"""
@dataclass      # So we use this dataclass decorator as insread of creating all that class and self and init method it'll do this task for us automtically.
class QueueEntry:       
    task_id: int
    original_priority: TaskPriority
    effective_priority: TaskPriority    # Priority currently used by the scheduler.During the Aging phase, this value may change from LOW -> MEDIUM -> HIGH.
    enqueued_at: datetime = field(default_factory=datetime.utcnow) # Timestamp when the task entered the queue created automatically when a QueueEntry object is created.
    last_priority_update_at: datetime = field(default_factory=datetime.utcnow)
    
    def get_waiting_time(self):
        waiting_time_since_last_update = datetime.utcnow() - self.last_priority_update_at
        return waiting_time_since_last_update.total_seconds()   # Returns the differnce in the seconds format.
        
