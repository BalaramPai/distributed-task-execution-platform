# src/service/taskService.py

from sqlalchemy.orm import Session

from src.utilities.response import error_response
from src.schemas.taskSchema import TaskCreateRequestSchema,TaskResponseSchema,TaskUpdateRequestScehma,TaskStatusUpdateRequestSchema
from src.models.taskModel import Task
from src.dao.taskDao import create_task,get_all_tasks,get_task,delete_task,update_task


def create_task_service(
    db: Session,
    task: TaskCreateRequestSchema
):

    # Used in create as there is no exisitng row. 
    task_model = Task(
        title=task.title,
        description=task.description,
        duration=task.duration,
        location=task.location,
        due_date=task.dueDate
    )

    saved_task = create_task(db,task_model)
    
    return TaskResponseSchema(
        id=saved_task.id,
        title=saved_task.title,
        description=saved_task.description,
        duration=saved_task.duration,
        location=saved_task.location,
        dueDate=saved_task.due_date,
        status=saved_task.status,
        createdAt=saved_task.created_at
        )
    
def get_all_tasks_service(db:Session,status:str,page:int,limit:int,search:str,sort:str):
    
    response_all_tasks = []
    
    all_tasks = get_all_tasks(db,status,page,limit,search,sort)
    
    
    for task in all_tasks:
        response_all_tasks.append(
            TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            status=task.status,
            createdAt=task.created_at
            )
        )

    return response_all_tasks


def get_task_service( db:Session, id : int):
    
    task = get_task(db,id)
    
    if task is None:
        return None
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            status=task.status,
            createdAt=task.created_at
            )
     
def delete_task_service(db:Session,id:int):
    
    task = delete_task(db,id)
    
    if task is None:
        return None
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            status=task.status,
            createdAt=task.created_at
            )
    
def update_task_service(db:Session,updated_task:TaskUpdateRequestScehma,id:int):
    
    task = get_task(db,id)
    
    if task is None:
        return None
    
    if updated_task.title is not None:
        task.title = updated_task.title
        
    if updated_task.description is not None:
        task.description = updated_task.description
    
    if updated_task.duration is not None:
        task.duration = updated_task.duration
        
    if updated_task.location is not None:
        task.location = updated_task.location
        
    if updated_task.dueDate is not None:
        task.due_date = updated_task.dueDate
    
    update_task(db,task)
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            status=task.status,
            createdAt=task.created_at
            )
    

def update_status_service(db:Session,updated_task:TaskStatusUpdateRequestSchema,id:int):
    
    task = get_task(db,id)
    
    if task is None:
        return None
    
    task.status = updated_task.status
        
    update_task(db,task)
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            status=task.status,
            createdAt=task.created_at
            )
    
    
    
    
    
    
    