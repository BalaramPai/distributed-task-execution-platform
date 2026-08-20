# src/schemas/schedulerSchema.py
from pydantic import BaseModel, Field
from datetime import datetime
from src.schemas.enums import (
    TaskPriority,
    WorkerState
)
from typing import List


class SchedulerStatusResponseSchema(BaseModel):
    queue_size : int
    dead_letter_queue_size : int
    worker_count : int
    running_tasks : int
    
    idle_workers : int
    busy_workers : int
    
    completed_tasks : int
    failed_tasks : int
    retried_tasks : int
    # uptime : time
    # scheduler_state : SchedulerStatus
    
# Schema for a single Task.    
class SchedulerTaskSchema(BaseModel):
    task_id: int
    priority: TaskPriority
    
# Schema to convert the above schemas into a list.
class SchedulerTasksResponseSchema(BaseModel):
    tasks: List[SchedulerTaskSchema]
    
# Schema for a single Worker. 
class SchedulerWorkerSchema(BaseModel):
    worker_id : int
    name : str
    is_alive : bool
    state : WorkerState
    current_task : int | None
    tasks_executed : int
    successful_tasks : int
    failed_tasks : int
    retried_tasks : int
    last_heartbeat: datetime
    is_healthy: bool 

# Schema for list of workers.
class SchedulerWorkersResponseSchema(BaseModel):
    workers: List[SchedulerWorkerSchema]

# Schema for scaling workers.
class SchedulerScaleRequestSchema(BaseModel):
    count: int = Field(..., ge=1)
    
class SchedulerScaleResponseSchema(BaseModel):
    previous_worker_count: int
    requested_worker_count: int
    current_worker_count: int
    scaling_action: str
    workers_changed: int