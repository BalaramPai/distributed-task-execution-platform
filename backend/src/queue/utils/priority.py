# src/queue/utils/priority.py

from src.schemas.enums import TaskPriority

PRIORITY_MAP = {
    TaskPriority.HIGH: 1,
    TaskPriority.MEDIUM: 2,
    TaskPriority.LOW: 3,
}