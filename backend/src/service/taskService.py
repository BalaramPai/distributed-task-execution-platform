# src/service/taskService.py

from sqlalchemy.orm import Session

from src.schemas.taskSchema import TaskCreateRequest
from src.models.taskModel import Task
from src.dao.taskDao import create_task


def create_task_service(
    db: Session,
    task: TaskCreateRequest
):

    task_model = Task(
        title=task.title,
        description=task.description,
        duration=task.duration,
        location=task.location,
        due_date=task.dueDate
    )

    return create_task(db,task_model)
    
    
    