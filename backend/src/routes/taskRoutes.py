# src/routes/taskRoutes.py

from fastapi import APIRouter
from src.controllers.taskController import create_task_controller
from src.schemas.taskSchema import TaskCreateRequest

router = APIRouter()

@router.post("/tasks")
def create_task(task:TaskCreateRequest):
    return create_task_controller(task)