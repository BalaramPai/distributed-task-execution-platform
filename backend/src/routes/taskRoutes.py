# src/routes/taskRoutes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.taskController import create_task_controller
from src.schemas.taskSchema import TaskCreateRequest
from src.database.database import get_db

router = APIRouter()


@router.post("/tasks")
def create_task(
    task: TaskCreateRequest,
    db: Session = Depends(get_db)
):

    return create_task_controller(db,task)