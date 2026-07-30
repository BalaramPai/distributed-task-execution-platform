# src/service/dependencyService.py
from sqlalchemy.orm import Session
from src.schemas.enums import TaskStatus

from src.exceptions.dependencyExceptions import (
    DuplicateDependencyError,
    InvalidDependencyError,
    DependencyNotFoundError,
    SelfDependencyError,
    CircularDependencyError
)

from src.dao.dependencyDao import (
    dependency_exists,
    get_dependencies,
    get_task_by_id
)



# 1. 
def validate_dependencies(db: Session,
                          dependencies: list[int],
                          task_id: int = None):
    # Duplicate dependency validation.
    if len(dependencies) != len(set(dependencies)):
        raise DuplicateDependencyError(
            "Duplicate dependency IDs are not allowed.")
      

    for dependency_id in dependencies:
        
        # Invalid dependency ID validation.
        if dependency_id <= 0:
            raise InvalidDependencyError(
                "Dependency IDs must be greater than 0.")
                
        # Self dependency validation.
        if task_id is not None and dependency_id == task_id:
            raise SelfDependencyError(task_id)
        
        # Dependency exists validation.
        if not dependency_exists(db,dependency_id):
                    raise DependencyNotFoundError(dependency_id)
                
        # Circular dependency validation.
        if task_id is not None:
            if can_reach_task(
                db,
                dependency_id,
                task_id,
                set()
            ):
                raise CircularDependencyError()


# 2.        
def are_dependencies_completed(db:Session,dependencies: list[int]):
    
    for dependency_id in dependencies:
        task_to_check = get_task_by_id(db,dependency_id)
        
        if task_to_check.status != TaskStatus.COMPLETED:
            return False            
    return True


# 3. This function checks if the current task and the dependency form a cycle by reverse method so it check if we reach the dependency from task and then goes above to validation logic.
def can_reach_task(
    db: Session,
    current_task: int,
    target_task: int,
    visited: set[int]
):
    if current_task == target_task:
        return True

    if current_task in visited:
        return False

    visited.add(current_task)

    dependencies = get_dependencies(db, current_task)

    for dependency in dependencies:
        if can_reach_task(db, dependency, target_task, visited):
            return True

    return False  