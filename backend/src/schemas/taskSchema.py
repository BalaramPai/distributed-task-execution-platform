# src/schemas/taskSchema.py

from pydantic import BaseModel, Field
from datetime import datetime,date
from src.schemas.enums import TaskStatus, TaskPriority
from typing import List


class TaskCreateRequestSchema(BaseModel):
    title : str = Field(min_length=3,max_length=100)
    description : str | None = Field(default=None,max_length=500)
    duration : int = Field(gt=0)
    location : str = Field(min_length=3,max_length=100)
    dueDate : date 
    priority : TaskPriority = TaskPriority.MEDIUM
    dependencies : List[int] = Field(default_factory=list)  #This default_factory option creates a new list every time rather than sharing the same list over and over again.
    
    
class TaskResponseSchema(BaseModel):
    id : int
    title : str
    description : str | None = None
    duration : int
    location : str | None = None
    dueDate : date | None = None
    status : TaskStatus
    priority : TaskPriority
    createdAt : datetime
    retry_count : int
    dependencies : List[int]
    
    
class TaskUpdateRequestSchema(BaseModel):
    title: str | None = Field(default=None,min_length=3,max_length=100)
    description: str |None = Field(default=None,max_length=500)
    duration: int | None = Field(default=None,gt=0)
    location: str | None = Field(default=None,min_length=3,max_length=100)
    dueDate: date | None = None
    priority : TaskPriority | None = None
    dependencies: List[int] | None = None
   
    
class TaskStatusUpdateRequestSchema(BaseModel):
    status: TaskStatus
 
    
class BulkTaskCreateRequestSchema(BaseModel):
    tasks: List[TaskCreateRequestSchema]

class BulkTaskResponseSchema(BaseModel):
    count: int
    tasks: List[TaskResponseSchema]