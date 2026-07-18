# src/schemas/schedulerSchema.py
from pydantic import BaseModel, Field
from datetime import time
from src.schemas.enums import TaskPriority
from typing import List


class SchedulerStatusResponseSchema(BaseModel):
    queue_size : int
    dead_letter_queue_size : int
    worker_count : int
    running_tasks : int
    # idle_workers : int
    # completed_tasks : int
    # failed_tasks : int
    # uptime : time
    # scheduler_state : SchedulerStatus
    
# Schema for a single Task.    
class SchedulerTaskSchema(BaseModel):
    task_id: int
    priority: TaskPriority
    
# Schema to convert the above schemas into a list.
class SchedulerTasksResponseSchema(BaseModel):
    tasks: List[SchedulerTaskSchema]