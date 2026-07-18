# src/controllers/schedulerController.py

from src.service.schedulerService import (
    get_scheduler_status_service,
    get_scheduler_tasks_service
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