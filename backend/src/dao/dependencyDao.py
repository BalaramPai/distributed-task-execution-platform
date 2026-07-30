# src/dao/dependencyDao.py

from sqlalchemy.orm import Session
from src.models.taskModel import Task


# To find if there is a task that exists for the particular dependency alloted to the task.    
def dependency_exists(db: Session, dependency_id: int):

    task = (
        db.query(Task)
        .where(Task.id == dependency_id)
        .first()
    )

    if task is None:
        return False

    return True

def get_dependencies(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        return []

    return task.dependencies

# To retrieve a single task from the database for the worker.
def get_task_by_id(db:Session,id:int):
    return db.query(Task).where(Task.id == id).first()