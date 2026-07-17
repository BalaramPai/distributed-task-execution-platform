# src/schemas/schedulerSchema.py
from pydantic import BaseModel, Field
from datetime import time
from src.schemas.enums import SchedulerStatus


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