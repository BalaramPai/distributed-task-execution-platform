# src/schemas/taskSchema.py

from pydantic import BaseModel, Field
from datetime import datetime,date

# Helper Enums Class (i.e. Datatype for Validation of Status like Field from pydantic for other fields.)
from enum import StrEnum
class AllowedStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"


class TaskCreateRequestSchema(BaseModel):
    title : str = Field(min_length=3,max_length=100)
    description : str | None = Field(default=None,max_length=500)
    duration : int = Field(gt=0)
    location : str = Field(min_length=3,max_length=100)
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
    
    
class TaskUpdateRequestScehma(BaseModel):
    title: str | None = Field(default=None,min_length=3,max_length=100)
    description: str |None = Field(default=None,max_length=500)
    duration: int | None = Field(default=None,gt=0)
    location: str | None = Field(default=None,min_length=3,max_length=100)
    dueDate: date | None = None
   
    
class TaskStatusUpdateRequestSchema(BaseModel):
    status: AllowedStatus
    