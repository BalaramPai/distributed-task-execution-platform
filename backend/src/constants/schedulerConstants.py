# src/constants/schedulerConstants.py

from src.schemas.enums import TaskPriority

# To Prevent typos which are only found at runtime.
THRESHOLD = "threshold"
PROMOTE_TO = "promote_to"

AGING_RULES = {
    TaskPriority.LOW: {
        THRESHOLD: 30,
        PROMOTE_TO: TaskPriority.MEDIUM,
    },
    TaskPriority.MEDIUM: {
        THRESHOLD: 60,
        PROMOTE_TO: TaskPriority.HIGH,
    },
    TaskPriority.HIGH: {
        THRESHOLD: None,
        PROMOTE_TO: None,
    },
}