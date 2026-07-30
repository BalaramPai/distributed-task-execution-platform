# src/dao.taskDao.py

from sqlalchemy.orm import Session
from src.models.taskModel import Task
from src.models.userModel import User
from src.schemas.enums import TaskStatus

# To create a task and insert it into the database.
def create_task(db:Session,task:Task):
    db.add(task)
    db.commit()
    db.refresh(task)   
    return task



# To retrieve all the tasks in the database.
def get_all_tasks(db:Session,status:str,page:int,limit:int,search:str,sort:str,owner_id: int):
    
    query = db.query(Task)
    query = query.where(Task.owner_id == owner_id)
    
    if status is not None:
        query = query.where(Task.status == status)
    if search is not None:
        query = query.where(Task.title.ilike(f"%{search}%"))
        
    if sort is not None:
        if sort[0] == '-':
            sort = sort[1:]
            value = getattr(Task,sort)
            
            query = query.order_by(value.desc())
        else:
            value = getattr(Task,sort)
            
            query = query.order_by(value.asc())
        
        
    return query.offset((page-1)*limit).limit(limit).all()




# To retrieve a single task from the database.(Authenticated and Authorised)
def get_task(db:Session,id : int,owner_id: int):
    return (
        db.query(Task)
        .where(
            Task.id == id,
            Task.owner_id == owner_id
        )
        .first()
    )

# To retrieve a single task from the database for the worker.
def get_task_for_worker(db:Session,id:int):
    return db.query(Task).where(Task.id == id).first()

# To get all tasks that are in Waiting State.
def get_waiting_tasks(db: Session):
    return (
        db.query(Task)
        .filter(Task.status == TaskStatus.WAITING)
        .all()
    )

def delete_task(db: Session,task: Task):

    db.delete(task)
    db.commit()
    return task



def update_task(db:Session,task:Task):
    db.commit()
    db.refresh(task)
    
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