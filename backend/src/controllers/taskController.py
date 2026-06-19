# src/controllers/taskController.py

from sqlalchemy.orm import Session

from src.service.taskService import (
    create_task_service,
    get_all_tasks_service,
    get_task_service,
    delete_task_service,
    update_task_service)
from src.schemas.taskSchema import TaskCreateRequestSchema,TaskUpdateRequestScehma
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
        

def get_task_controller(db:Session, id : int):
    try:
        task_response = get_task_service(db,id)
        
        if task_response == None:
            return error_response(message=f"No such task with ID {id} exists")
        
        return success_response(
            message = f"Task wit ID {id} has been retrieved.",
            data = task_response 
        )
    except Exception as e:
        return error_response(
            message = "Failed to retrieve the task.",
            error = str(e)
        )
        
def delete_task_controller(db:Session,id:int):
    try:
        task = delete_task_service(db,id)
        
        if task == None:
            return error_response(message=f"No such task with ID {id} exists to be deleted.")
        
        return success_response(
            message = f"Task with ID {id} has been deleted successfully.",
            data = task
        )
    
    except Exception as e:
        return error_response(
            message = "Failed to delete the task.",
            error = str(e)
        )
        

def update_task_controller(db:Session,task:TaskUpdateRequestScehma,id:int):
    try:
        task = update_task_service(db,task,id)
        
        if task == None:
            return error_response(message=f"No such task with ID {id} to update.")
        
        return success_response(message=f"Task with the ID {id} has been updates successfully.",data=task)
    
    except Exception as e:
        return error_response(
            message = "Failed to update the task.",
            error = str(e)
        )
        
        
