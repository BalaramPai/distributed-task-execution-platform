# src/routes/taskRoutes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.taskController import (
    create_task_controller,
    get_all_tasks_controller,
    get_task_controller,
    delete_task_controller,
    update_task_controller,
    update_status_controller)
from src.schemas.taskSchema import (
    TaskCreateRequestSchema,
    TaskUpdateRequestScehma,
    TaskStatusUpdateRequestSchema)
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
    status : str | None=None,
    page : int=1,
    limit : int =10,
    search : str | None=None,
    db : Session = Depends(get_db)
):
        return get_all_tasks_controller(db,status,page,limit,search)



    
@router.get("/task/{id}")
def get_task(
    id : int,
    db : Session = Depends(get_db)
):
    return get_task_controller(db,id)

@router.delete("/task/{id}")
def delete_task(
    id: int,
    db:Session = Depends(get_db)
):
    return delete_task_controller(db,id)

@router.put("/task/{id}")
def update_task(
    id: int,
    task : TaskUpdateRequestScehma,
    db : Session = Depends(get_db)
):
    return update_task_controller(db,task,id)

@router.patch("/task/{id}/status")
def update_status(
    id :int,
    task : TaskStatusUpdateRequestSchema,
    db : Session = Depends(get_db)
):
    return update_status_controller(db,task,id)