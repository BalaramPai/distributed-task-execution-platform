# src/controllers/taskController.py

from sqlalchemy.orm import Session

from src.service.taskService import create_task_service,get_all_tasks_service
from src.schemas.taskSchema import TaskCreateRequestSchema
from src.utilities.response import (
    success_response,
    error_response
)


def create_task_controller(
    db: Session,
    task: TaskCreateRequestSchema
):

    try:

        task_response = create_task_service(db,task)

        return success_response(
            message="Task has been created successfully",
            data=task_response
        )

    except Exception as e:

        return error_response(
            message="Task creation failed",
            error=str(e)
        )
        
        
def get_all_tasks_controller(
    db: Session,
):

    try:

        task_response = get_all_tasks_service(db)

        return success_response(
            message="Tasks fetched successfully",
            data= {"count":len(task_response),"tasks":task_response}
        )

    except Exception as e:

        return error_response(
            message="All Tasks retrieval failed",
            error=str(e)
        )
        
