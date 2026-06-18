# src/controllers/taskController.py

from sqlalchemy.orm import Session

from src.service.taskService import create_task_service
from src.schemas.taskSchema import TaskCreateRequest
from src.utilities.response import (
    success_response,
    error_response
)


def create_task_controller(
    db: Session,
    task: TaskCreateRequest
):

    try:

        task_response = create_task_service(
            db,
            task
        )

        return success_response(
            message="Task has been created successfully",
            data=task_response
        )

    except Exception as e:

        return error_response(
            message="Task creation failed",
            error=str(e)
        )