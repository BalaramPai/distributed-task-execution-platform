# src/controllers/taskController.py

from src.service.taskService import create_task_service
from src.schemas.taskSchema import TaskCreateRequest
from src.utilities.response import success_response,error_response

def create_task_controller(task : TaskCreateRequest):
    try:
        task_response = create_task_service(task)
        return success_response(message="Task has been created successfully",data=task_response)
    except Exception as e:
        return error_response(error=str(e))