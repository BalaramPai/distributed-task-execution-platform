# src/routes/schedulerRoutes.py

# GET  /scheduler/status
# GET  /scheduler/tasks
# GET  /scheduler/workers
# GET  /scheduler/workers/{id}
# GET  /scheduler/metrics

# POST /scheduler/pause
# POST /scheduler/resume
# POST /scheduler/rebalance

# DELETE /scheduler/queue

# GET  /scheduler/starvation
# GET  /scheduler/aging

from fastapi import APIRouter
from src.controllers.schedulerController import (
    get_scheduler_status_controller,
    get_scheduler_tasks_controller,
    get_scheduler_worker_controller,
    get_scheduler_all_workers_controller,
    scale_scheduler_workers_controller
    )
from src.schemas.schedulerSchema import SchedulerScaleRequestSchema

router = APIRouter(tags=["Scheduler Flow"])


# "What is the scheduler's current overall situation?"
@router.get("/scheduler/status")
def get_scheduler_status():
    return get_scheduler_status_controller()


# "What tasks are currently sitting in the runtime queue?"
@router.get("/scheduler/tasks")
def get_scheduler_tasks():
    return get_scheduler_tasks_controller()

# "Show me all the workers currently managed by the scheduler."
@router.get("/scheduler/workers")
def get_scheduler_worker_list():
    return get_scheduler_all_workers_controller()

# "Give me detailed information about Worker 3."
@router.get("/scheduler/workers/{worker_id}")
def get_scheduler_worker(worker_id: int):
    return get_scheduler_worker_controller(worker_id)

# Scales the workers and gives data output based on the scaling.
@router.post("/scheduler/workers/scale")
def scale_workers(request:SchedulerScaleRequestSchema):
    return scale_scheduler_workers_controller(request.count)
