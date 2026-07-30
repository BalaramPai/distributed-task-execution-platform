# src/schemas/dependencySchema.py
from pydantic import BaseModel
from src.schemas.enums import TaskStatus


class DependencyInfoSchema(BaseModel):
    id: int
    title: str
    status: TaskStatus


class TaskDependenciesResponseSchema(BaseModel):
    task_id: int
    dependencies: list[DependencyInfoSchema]


class BlockedDependencySchema(BaseModel):
    id: int
    title: str
    status: TaskStatus


class BlockedReasonResponseSchema(BaseModel):
    task_id: int
    status: TaskStatus
    blocked_by: list[BlockedDependencySchema]