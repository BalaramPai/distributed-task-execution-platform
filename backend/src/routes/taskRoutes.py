# src/routes/taskRoutes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.taskController import (
    create_task_controller,
    get_all_tasks_controller,
    get_task_controller,
    delete_task_controller,
    update_task_controller,
    update_status_controller,
    create_bulk_tasks_controller
    )

from src.schemas.taskSchema import (
    TaskCreateRequestSchema,
    TaskUpdateRequestSchema,
    TaskStatusUpdateRequestSchema,
    BulkTaskCreateRequestSchema)

from src.database.database import get_db

from src.dependencies.auth import get_current_user

router = APIRouter(tags=["Task Flow"])


@router.post("/tasks")
def create_task(
    task: TaskCreateRequestSchema,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_task_controller(db,task,current_user)



@router.get("/tasks")
def get_all_tasks(
    sort:str | None = None,
    status : str | None=None,
    page : int=1,
    limit : int =10,
    search : str | None=None,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
        return get_all_tasks_controller(db,status,page,limit,search,sort,current_user)



    
@router.get("/task/{id}")
def get_task(
    id : int,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return get_task_controller(db,id,current_user)

@router.delete("/task/{id}")
def delete_task(
    id: int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    return delete_task_controller(db,id,current_user)

@router.put("/task/{id}")
def update_task(
    id: int,
    task : TaskUpdateRequestSchema,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return update_task_controller(db,task,id,current_user)

@router.patch("/task/{id}/status")
def update_status(
    id :int,
    task : TaskStatusUpdateRequestSchema,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return update_status_controller(db,task,id,current_user)

@router.post("/tasks/bulk")
def create_bulk_tasks(
    tasks: BulkTaskCreateRequestSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_bulk_tasks_controller(db,tasks,current_user)