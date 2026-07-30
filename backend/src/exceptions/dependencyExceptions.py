# src/exceptions/dependencyExceptions.py
"""
Dependency Validation Exceptions

These exceptions are raised while creating or updating tasks
when dependency validation fails.
"""


class DependencyValidationError(Exception):
    """
    Base exception for all dependency validation errors.
    """

    def __init__(self, message: str = "Dependency validation failed"):
        self.message = message
        super().__init__(self.message)


class DuplicateDependencyError(DependencyValidationError):
    def __init__(self, message: str = "Duplicate dependency IDs are not allowed"):
        super().__init__(message)


class InvalidDependencyError(DependencyValidationError):
    def __init__(self, message: str = "Invalid dependency ID"):
        super().__init__(message)


class DependencyNotFoundError(DependencyValidationError):
    def __init__(self, dependency_id: int):
        super().__init__(
            f"Dependency task with ID {dependency_id} does not exist."
        )

class SelfDependencyError(DependencyValidationError):

    def __init__(self, task_id: int):
        super().__init__(
            f"Task with ID {task_id} cannot depend on itself."
        )
        
class CircularDependencyError(Exception):
    def __init__(self):
        super().__init__("Circular dependency detected.")