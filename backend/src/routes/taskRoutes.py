# src/routes/taskRoutes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.taskController import create_task_controller,get_all_tasks_controller
from src.schemas.taskSchema import TaskCreateRequestSchema
from src.database.database import get_db

router = APIRouter()


@router.post("/tasks")
def create_task(
    task: TaskCreateRequestSchema,
    db: Session = Depends(get_db)
):

    return create_task_controller(db,task)

@router.get("/tasks")
def get_all_tasks(
    db : Session = Depends(get_db)
):
        return get_all_tasks_controller(db)