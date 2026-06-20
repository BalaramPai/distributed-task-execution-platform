# src/dao.taskDao.py

from sqlalchemy.orm import Session
from src.models.taskModel import Task

# To create a task and insert it into the database.
def create_task(db:Session,task:Task):
    db.add(task)
    db.commit()
    db.refresh(task)   
    return task

# To retrieve all the tasks in the database.
def get_all_tasks(db:Session,status:str):
    if status is None:
        return db.query(Task).all()
    return db.query(Task).where(Task.status == status).all()

# To retrieve a single task from the database.
def get_task(db:Session,id : int):
    return db.query(Task).where(Task.id == id).first()

def delete_task(db:Session,id:int):
    
    task = get_task(db,id)
    
    if task is None:
        return None
    else:
        db.delete(task)
        db.commit()
    
    return task

def update_task(db:Session,task:Task):
    db.commit()
    db.refresh(task)