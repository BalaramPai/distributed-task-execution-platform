# src/routes/schedulerRoutes.py

# GET  /scheduler/status
# GET  /scheduler/tasks
# GET  /scheduler/workers
# GET  /scheduler/metrics

# POST /scheduler/pause
# POST /scheduler/resume
# POST /scheduler/rebalance

# DELETE /scheduler/queue

# GET  /scheduler/starvation
# GET  /scheduler/aging

from fastapi import APIRouter, Depends
from src.controllers.schedulerController import (
    get_scheduler_status_controller,
    get_scheduler_tasks_controller
    )

router = APIRouter(tags=["Scheduler Flow"])


@router.get("/scheduler/status")
def get_scheduler_status():
    return get_scheduler_status_controller()


@router.get("/scheduler/tasks")
def get_scheduler_tasks():
    return get_scheduler_tasks_controller()
