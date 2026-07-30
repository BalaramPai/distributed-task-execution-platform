from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.controllers.dependencyController import (
    get_task_dependencies_controller,
    get_blocked_reason_controller
)

router = APIRouter(tags=["Dependency"])

@router.get("/dependency/{task_id}")
def get_task_dependencies(
    task_id: int,
    db: Session = Depends(get_db)
):
    return get_task_dependencies_controller(db, task_id)

@router.get("/dependency/{task_id}/blocked-by")
def get_blocked_reason(
    task_id: int,
    db: Session = Depends(get_db)
):
    return get_blocked_reason_controller(db, task_id)