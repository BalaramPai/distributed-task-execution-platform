# src/models/taskModel.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    JSON
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy import Enum

from src.database.base import Base
from src.schemas.enums import TaskPriority,TaskStatus


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text)

    duration = Column(Integer, nullable=False)

    location = Column(String(255))

    due_date = Column(Date)
    
    priority = Column(
        Enum(TaskPriority),
        nullable=False,
        default=TaskPriority.MEDIUM
    )

    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.QUEUED
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    
    owner_id = Column(
    Integer,
    ForeignKey("users.id"),
    nullable=False
    )
    
    retry_count = Column(Integer, default=0)
    
    dependencies = Column(
        JSON,
        nullable=False,
        default=list
    )  
    
    owner = relationship(
        "User",
        back_populates="tasks"
        )