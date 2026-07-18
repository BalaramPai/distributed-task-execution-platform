# src/service/schedulerService.py

from src.queue.queueManager import task_queue,dead_letter_queue     # For the stats we will need the queues(heaps).
from src.workers.workerManager import (
    get_worker_count,   # Gives the total number of workers available.
    get_running_tasks   # Gives the total number of active tasks.
)
from src.schemas.schedulerSchema import (
    SchedulerStatusResponseSchema,   # Response schema for schedule status.
    SchedulerTasksResponseSchema
)

def get_scheduler_status_service():
    
    return SchedulerStatusResponseSchema (
        queue_size = task_queue.size(),
        dead_letter_queue_size = dead_letter_queue.size(),
        worker_count = get_worker_count(),
        running_tasks = get_running_tasks()
    )
    
def get_scheduler_tasks_service():
    
    return SchedulerTasksResponseSchema (
        tasks = task_queue.get_queue_snapshot()
    )