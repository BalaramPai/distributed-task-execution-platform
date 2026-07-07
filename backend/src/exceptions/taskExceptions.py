# src/exceptions/taskExceptions.py

"""
Task Execution Exceptions

These exceptions are used by the task execution engine to classify failures.

TransientTaskError:
    Temporary failures that may succeed if retried.

PermanentTaskError:
    Non-recoverable failures that should not be retried.
"""


class TaskExecutionError(Exception):
    """
    Base exception for all task execution related errors.
    """

    def __init__(self, message: str = "Task execution failed"):
        self.message = message
        super().__init__(self.message)


class TransientTaskError(TaskExecutionError):
    """
    Temporary failure.

    Examples:
    - Network timeout
    - Database temporarily unavailable
    - External API unavailable
    - Connection reset

    These failures SHOULD be retried.
    """

    def __init__(self, message: str = "Transient task execution failure"):
        super().__init__(message)


class PermanentTaskError(TaskExecutionError):
    """
    Permanent failure.

    Examples:
    - Invalid input
    - Validation failure
    - Programming error
    - Invalid task configuration

    These failures SHOULD NOT be retried.
    """

    def __init__(self, message: str = "Permanent task execution failure"):
        super().__init__(message)