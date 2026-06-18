# src/dao.taskDao.py

from sqlalchemy.orm import Session
from src.models.taskModel import Task

def create_task(db:Session,task:Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

