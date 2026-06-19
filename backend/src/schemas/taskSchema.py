# src/schemas/taskSchema.py

from pydantic import BaseModel
from datetime import datetime,date

class TaskCreateRequestSchema(BaseModel):
    title : str
    description : str | None = None
    duration : int
    location : str
    dueDate : date
    
    
class TaskResponseSchema(BaseModel):
    id : int
    title : str
    description : str | None = None
    duration : int
    location : str | None = None
    dueDate : date | None = None
    status : str
    createdAt : datetime
    
    