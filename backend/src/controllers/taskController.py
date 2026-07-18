# src/controllers/taskController.py

from sqlalchemy.orm import Session

from src.service.taskService import (
    create_task_service,
    get_all_tasks_service,
    get_task_service,
    delete_task_service,
    update_task_service,
    update_status_service,
    create_bulk_tasks_service
    )

from src.schemas.taskSchema import (
    TaskCreateRequestSchema,
    TaskUpdateRequestSchema,
    TaskStatusUpdateRequestSchema,
    BulkTaskCreateRequestSchema
    )
from src.utilities.response import (
    success_response,
    error_response
)


from src.models.userModel import User


def create_task_controller(
    db: Session,
    task: TaskCreateRequestSchema,
    current_user: User
):

    try:

        task_response = create_task_service(db,task,current_user)

        return success_response(
            message="Task has been created successfully",
            data=task_response,
            status_code=201
        )

    except Exception as e:

        return error_response(
            message="Task creation failed",
            error=str(e)
        )
        
        
def get_all_tasks_controller(
    db: Session,
    status: str,
    page: int,
    limit: int,
    search: str,
    sort: str,
    current_user: User
):

    try:

        task_response = get_all_tasks_service(db,status,page,limit,search,sort,current_user)
        
        if status is None:
            return success_response(
                message="Tasks fetched successfully",
                data= {"count":len(task_response),"tasks":task_response}
            )
        return success_response(
                message=f"{status} Tasks fetched successfully",
                data= {"count":len(task_response),"tasks":task_response}
            )

    except Exception as e:

        return error_response(
            message="All Tasks retrieval failed",
            error=str(e)
        )
        

def get_task_controller(db:Session, id : int,current_user: User):
    try:
        task_response = get_task_service(db,id,current_user)
        
        if task_response == None:
            return error_response(message=f"No such task with ID {id} exists",status_code=404)
        
        return success_response(
            message = f"Task wit ID {id} has been retrieved.",
            data = task_response 
        )
    except Exception as e:
        return error_response(
            message = "Failed to retrieve the task.",
            error = str(e)
        )
        
def delete_task_controller(db:Session,id:int,current_user: User):
    try:
        task = delete_task_service(db,id,current_user)
        
        if task == None:
            return error_response(message=f"No such task with ID {id} exists to be deleted.",status_code=404)
        
        return success_response(
            message = f"Task with ID {id} has been deleted successfully.",
            data = task
        )
    
    except Exception as e:
        return error_response(
            message = "Failed to delete the task.",
            error = str(e)
        )
        

def update_task_controller(db:Session,task:TaskUpdateRequestSchema,id:int,current_user: User):
    try:
        task = update_task_service(db,task,id,current_user)
        
        if task == None:
            return error_response(message=f"No such task with ID {id} to update.",status_code=404)
        
        return success_response(message=f"Task with the ID {id} has been updated successfully.",data=task)
    
    except Exception as e:
        return error_response(
            message = "Failed to update the task.",
            error = str(e)
        )

def update_status_controller(db:Session,task:TaskStatusUpdateRequestSchema,id:int,current_user: User):
    try:
        task = update_status_service(db,task,id,current_user)
        
        if task == None:
            return error_response(message=f"No such task with ID {id} to update.",status_code=404)
        
        return success_response(message=f"Task with the ID {id} has been updateD successfully.",data=task)
    
    except Exception as e:
        return error_response(
            message = "Failed to update the task.",
            error = str(e)
        )
            
def create_bulk_tasks_controller(db: Session,tasks: BulkTaskCreateRequestSchema,current_user: User):
    try:
        response = create_bulk_tasks_service(db,tasks,current_user)

        return success_response(
            message="Tasks created successfully.",
            data=response,
            status_code=201
        )

    except Exception as e:

        return error_response(
            message="Bulk task creation failed.",
            error=str(e)
        )
