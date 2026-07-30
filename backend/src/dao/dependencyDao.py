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


# To retrieve all dependency task objects.
def get_dependency_tasks(db: Session, dependency_ids: list[int]):
    return (
        db.query(Task)
        .filter(Task.id.in_(dependency_ids))
        .all()
    )


# To retrieve all tasks that depend on a particular task.
def get_dependent_tasks(db: Session, task_id: int):
    return (
        db.query(Task)
        .filter(Task.dependencies.contains([task_id]))
        .all()
    )