# src/models/taskModel.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


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
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )