# src/service/schedulerService.py

from src.queue.queueManager import (      # For the stats we will need the queues(heaps).
    task_queue,
    dead_letter_queue
    )
from src.workers.workerManager import (
    get_worker_count,   # Gives the total number of workers available.
    get_running_tasks,  # Gives the total number of active tasks.
    get_worker,
    get_all_workers,
    get_worker_count_by_state,
    get_total_failed_tasks,
    get_total_retried_tasks,
    get_total_successful_tasks
)
from src.schemas.schedulerSchema import (
    SchedulerStatusResponseSchema,   # Response schema for schedule status.
    SchedulerTasksResponseSchema,
    SchedulerWorkerSchema,
    SchedulerWorkersResponseSchema
)
from src.schemas.enums import WorkerState

def get_scheduler_status_service():
    
    return SchedulerStatusResponseSchema (
        queue_size = task_queue.size(),
        dead_letter_queue_size = dead_letter_queue.size(),
        worker_count = get_worker_count(),
        running_tasks = get_running_tasks(),
        idle_workers = get_worker_count_by_state(WorkerState.IDLE),
        busy_workers = get_worker_count_by_state(WorkerState.BUSY),
        completed_tasks = get_total_successful_tasks(),
        failed_tasks = get_total_failed_tasks(),
        retried_tasks = get_total_retried_tasks(),
    )
    
def get_scheduler_tasks_service():
    
    return SchedulerTasksResponseSchema (
        tasks = task_queue.get_queue_snapshot()
    )
    
    
def get_scheduler_worker_service(worker_id:int):
    
    worker = get_worker(worker_id)
    
    if worker is None:
        return None
    
    return SchedulerWorkerSchema(
        worker_id=worker.worker_id,
        name=worker.name,
        is_alive=worker.is_alive(),
        state=worker.state,
        current_task=worker.current_task,
        tasks_executed=worker.tasks_executed,
        successful_tasks=worker.successful_tasks,
        failed_tasks=worker.failed_tasks,
        retried_tasks=worker.retried_tasks,
    )
    
def get_scheduler_all_workers_service():
    
    worker_list = []

    for worker in get_all_workers():
        worker_list.append(
            SchedulerWorkerSchema(
                worker_id=worker.worker_id,
                name=worker.name,
                is_alive=worker.is_alive(),
                state=worker.state,
                current_task=worker.current_task,
                tasks_executed=worker.tasks_executed,
                successful_tasks=worker.successful_tasks,
                failed_tasks=worker.failed_tasks,
                retried_tasks=worker.retried_tasks,
            )
        )

    return SchedulerWorkersResponseSchema(workers=worker_list)