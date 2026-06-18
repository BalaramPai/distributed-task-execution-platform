# src/schemas/taskSchema.py

from pydantic import BaseModel
from datetime import datetime,date

class TaskCreateRequest(BaseModel):
    title : str
    description : str | None = None
    duration : int
    location : str
    dueDate : date
    
    
class TaskResponse(BaseModel):
    id : int
    title : str
    description : str | None = None
    duration : int
    location : str
    dueDate : date
    status : str
    createdAt : datetime
    
    