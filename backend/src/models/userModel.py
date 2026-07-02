# src/models/userModel.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from src.database.base import Base

from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(Enum(UserRole),nullable=False,default=UserRole.USER)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tasks = relationship(
    "Task",
    back_populates="owner",
    cascade="all, delete-orphan"
)