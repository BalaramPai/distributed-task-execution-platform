# src/controllers/schedulerController.py

from src.service.schedulerService import (
    get_scheduler_status_service,
    get_scheduler_tasks_service,
    get_scheduler_worker_service,
    get_scheduler_all_workers_service,
    scale_scheduler_workers_service
    )
from src.utilities.response import success_response,error_response

def get_scheduler_status_controller():
    try:
        scheduler_response = get_scheduler_status_service()
        
        return success_response(
            message = "Scheduler status retrieved successfully.",
            data = scheduler_response
        )
    except Exception as e:
        return error_response(
            message = "Failed to retrieve the status.",
            error = str(e)
        )
        
def get_scheduler_tasks_controller():
    try:
        scheduler_response = get_scheduler_tasks_service()
        
        if len(scheduler_response.tasks) == 0:
            return success_response(
            message = "There are no tasks at the moment to retrieve.",
            data = scheduler_response
            )
            
        
        return success_response(
            message = "Scheduler tasks retrieved successfully.",
            data = scheduler_response
        )
    except Exception as e:
        return error_response(
            message = "Failed to retrieve the tasks.",
            error = str(e)
        )
        

def get_scheduler_worker_controller(worker_id: int):
    try:
        scheduler_response = get_scheduler_worker_service(worker_id)

        if scheduler_response is None:
            return error_response(
                message="Worker not found.",
                error=f"No worker exists with ID {worker_id}."
            )

        return success_response(
            message="Scheduler worker retrieved successfully.",
            data=scheduler_response
        )

    except Exception as e:
        return error_response(
            message="Failed to retrieve the worker.",
            error=str(e)
        )
        
def get_scheduler_all_workers_controller():
    try:
        scheduler_response = get_scheduler_all_workers_service()

        if len(scheduler_response.workers) == 0:
            return success_response(
                message="There are no workers at the moment to retrieve.",
                data=scheduler_response
            )

        return success_response(
            message="Scheduler workers retrieved successfully.",
            data=scheduler_response
        )

    except Exception as e:
        return error_response(
            message="Failed to retrieve the workers.",
            error=str(e)
        )
        
def scale_scheduler_workers_controller(count: int):
    try:
        scheduler_response = scale_scheduler_workers_service(count)

        if scheduler_response.scaling_action == "SCALE_UP":
            message = (
                f"Workers scaled up successfully by "
                f"{scheduler_response.workers_changed}."
            )

        elif scheduler_response.scaling_action == "SCALE_DOWN":
            message = (
                f"Workers scaled down successfully by "
                f"{scheduler_response.workers_changed}."
            )

        else:
            message = (
                f"Worker count is already set to "
                f"{scheduler_response.current_worker_count}."
            )

        return success_response(
            message=message,
            data=scheduler_response
        )

    except Exception as e:
        return error_response(
            message="Failed to scale the workers.",
            error=str(e)
        )