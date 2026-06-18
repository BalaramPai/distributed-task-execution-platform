# src/service/taskService.py

from src.schemas.taskSchema import TaskCreateRequest,TaskResponse
import random as rd
from datetime import datetime

def create_task_service(task : TaskCreateRequest):
    return TaskResponse(
        id = rd.randint(1000,9999),
        title = task.title,
        description=task.description,
        duration=task.duration,
        location=task.location,
        dueDate=task.dueDate,
        status="PENDING",
        createdAt=datetime.now()
    )
    
    
    
    