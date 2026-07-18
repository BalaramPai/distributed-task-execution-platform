# src/controllers/schedulerController.py

from src.service.schedulerService import get_scheduler_status_service
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