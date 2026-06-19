# src/service/taskService.py

from sqlalchemy.orm import Session

from src.schemas.taskSchema import TaskCreateRequestSchema,TaskResponseSchema
from src.models.taskModel import Task
from src.dao.taskDao import create_task,get_all_tasks


def create_task_service(
    db: Session,
    task: TaskCreateRequestSchema
):

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
    
def get_all_tasks_service(db:Session):
    
    response_all_tasks = []
    
    all_tasks = get_all_tasks(db)
    
    
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
        
    
    