# src/queue/utils/priority.py

from src.schemas.enums import TaskPriority

PRIORITY_MAP = {
    TaskPriority.HIGH: 1,
    TaskPriority.MEDIUM: 2,
    TaskPriority.LOW: 3,
}

REVERSE_PRIORITY_MAP = {
    1: TaskPriority.HIGH,
    2: TaskPriority.MEDIUM,
    3: TaskPriority.LOW,
}