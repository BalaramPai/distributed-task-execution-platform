# src/models/taskModel.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.base import Base


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text)

    duration = Column(Integer, nullable=False)

    location = Column(String(255))

    due_date = Column(Date)

    status = Column(
        String(20),
        nullable=False,
        default="QUEUED"
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
    
    owner = relationship(
    "User",
    back_populates="tasks"
    )
    
    retry_count = Column(Integer, default=0)