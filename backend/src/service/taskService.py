# src/service/taskService.py

from sqlalchemy.orm import Session

from src.schemas.taskSchema import (
    TaskCreateRequestSchema,
    TaskResponseSchema,
    TaskUpdateRequestSchema,
    TaskStatusUpdateRequestSchema,
    BulkTaskCreateRequestSchema,
    BulkTaskResponseSchema
    )
from src.schemas.enums import TaskStatus
from src.models.taskModel import Task
from src.dao.taskDao import ( 
    create_task,
    get_all_tasks,
    get_task,
    delete_task,
    update_task,
    get_task_for_worker,        # Simply fetches a task without need of extra params.
    dependency_exists,
    get_waiting_tasks,
    get_dependencies
    )
from src.queue.queueManager import task_queue,dead_letter_queue
from src.exceptions.taskExceptions import (
    TransientTaskError,
    PermanentTaskError,
    )
from src.exceptions.dependencyExceptions import (
    DuplicateDependencyError,
    InvalidDependencyError,
    DependencyNotFoundError,
    SelfDependencyError,
    CircularDependencyError
)

from time import sleep


from src.models.userModel import User
from src.constants.taskConstants import MAX_RETRIES

# Helper functions.
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
        task_to_check = get_task_for_worker(db,dependency_id)
        
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
             
#---------------------------------------------------------------------#   


def create_task_service(
    db: Session,
    task: TaskCreateRequestSchema,
    current_user: User
):
    validate_dependencies(db,task.dependencies)   

    # Used in create as there is no exisitng row. 
    task_model = Task(
        title=task.title,
        description=task.description,
        duration=task.duration,
        location=task.location,
        due_date=task.dueDate,
        owner_id=current_user.id,
        priority = task.priority,
        dependencies = task.dependencies
    )
    
    # We set the intital status here itself to prevent 2 database writes.
    if (not task.dependencies or are_dependencies_completed(db, task.dependencies)):
        task_model.status = TaskStatus.QUEUED
    else:
        task_model.status = TaskStatus.WAITING
        
    # The task gets to the database irresepective of the dependencies.
    saved_task = create_task(db,task_model)
    
    # If there are no dependencies in a task then it is enqueued.
    if saved_task.status == TaskStatus.QUEUED:
            task_queue.enqueue(saved_task.id,saved_task.priority)
    
    return TaskResponseSchema(
        id=saved_task.id,
        title=saved_task.title,
        description=saved_task.description,
        duration=saved_task.duration,
        location=saved_task.location,
        dueDate=saved_task.due_date,
        priority=saved_task.priority,
        status=saved_task.status,
        createdAt=saved_task.created_at,
        retry_count=saved_task.retry_count,
        dependencies=saved_task.dependencies,
        )
    
def get_all_tasks_service(db:Session,status:str,page:int,limit:int,search:str,sort:str,current_user: User):
    
    response_all_tasks = []
    
    all_tasks = get_all_tasks(db,status,page,limit,search,sort,current_user.id)
    
    
    for task in all_tasks:
        response_all_tasks.append(
            TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            priority=task.priority,
            status=task.status,
            createdAt=task.created_at,
            retry_count=task.retry_count,
            dependencies=task.dependencies,
            )
        )

    return response_all_tasks


def get_task_service( db:Session, id : int,current_user: User):
    
    task = get_task(db,id,current_user.id)
    
    if task is None:
        return None
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            priority=task.priority,
            status=task.status,
            createdAt=task.created_at,
            retry_count=task.retry_count,
            dependencies=task.dependencies,
            )
     
def delete_task_service(db: Session,id: int,current_user: User):

    task = get_task(db,id,current_user.id)

    if task is None:
        return None

    delete_task(db,task)

    return TaskResponseSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        duration=task.duration,
        location=task.location,
        dueDate=task.due_date,
        priority=task.priority,
        status=task.status,
        createdAt=task.created_at,
        retry_count=task.retry_count,
        dependencies=task.dependencies,
    )
    
def update_task_service(db:Session,updated_task:TaskUpdateRequestSchema,id:int,current_user: User):
    
    task = get_task(db,id,current_user.id)
    
    if task is None:
        return None
    
    if updated_task.title is not None:
        task.title = updated_task.title
        
    if updated_task.description is not None:
        task.description = updated_task.description
    
    if updated_task.duration is not None:
        task.duration = updated_task.duration
        
    if updated_task.location is not None:
        task.location = updated_task.location
        
    if updated_task.dueDate is not None:
        task.due_date = updated_task.dueDate
        
    if updated_task.priority is not None:
        task.priority = updated_task.priority
    
    if updated_task.dependencies is not None:
        validate_dependencies(db,updated_task.dependencies,id)
        task.dependencies = updated_task.dependencies
        
    
    update_task(db,task)
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            priority=task.priority,
            status=task.status,
            createdAt=task.created_at,
            retry_count=task.retry_count,
            dependencies=task.dependencies,
            )
    

def update_status_service(db:Session,updated_task:TaskStatusUpdateRequestSchema,id:int,current_user: User):
    
    task = get_task(db,id,current_user.id)
    
    if task is None:
        return None
    
    task.status = updated_task.status
        
    update_task(db,task)
    
    return TaskResponseSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            duration=task.duration,
            location=task.location,
            dueDate=task.due_date,
            priority=task.priority,
            status=task.status,
            createdAt=task.created_at,
            retry_count=task.retry_count,
            dependencies=task.dependencies,
            )

def create_bulk_tasks_service(db: Session,tasks: BulkTaskCreateRequestSchema,current_user: User):
    created_tasks = []

    for task in tasks.tasks:
        created_task = create_task_service(db,task,current_user)
        created_tasks.append(created_task)

    return BulkTaskResponseSchema(
        count=len(created_tasks),
        tasks=created_tasks
    )
    
def execute_task(db:Session,id:int):
    
    task = get_task_for_worker(db,id)
    
    if task is None:
        return None
    
    print(f"Task {id} is now IN_PROGRESS")
    task.status = TaskStatus.IN_PROGRESS
    
    update_task(db,task)
    
    sleep(5)
    
    print(f"Task {id} completed")
    task.status = TaskStatus.COMPLETED
        
    update_task(db,task)
    



def process_task(db: Session, task_id: int):
    """
    Handles task execution and retry logic.
    """

    try:
        execute_task(db, task_id)
        
        # Now we retrieve tasks that are in wait state.
        wait_task_list = get_waiting_tasks(db)
        
        # Here we update each task whose dependencies have been completed.
        for w_task in wait_task_list:
            if are_dependencies_completed(db,w_task.dependencies):
                w_task.status = TaskStatus.QUEUED
                update_task(db,w_task)
                task_queue.enqueue(w_task.id,w_task.priority)
                

    except TransientTaskError as e:
        print(f"Transient Error: {e}")

        task = get_task_for_worker(db, task_id)

        if task is None:
            return

        task.retry_count += 1

        if task.retry_count < MAX_RETRIES:

            print(
                f"Retrying Task {task.id} "
                f"({task.retry_count}/{MAX_RETRIES})"
            )

            task.status = TaskStatus.QUEUED

            update_task(db, task)

            task_queue.enqueue(task.id,task.priority)

        else:

            print(
                f"Task {task.id} exceeded maximum retries."
            )

            task.status = TaskStatus.FAILED

            update_task(db, task)

            dead_letter_queue.enqueue(task.id,task.priority)

    except PermanentTaskError as e:
        print(f"Permanent Error: {e}")

        task = get_task_for_worker(db, task_id)

        if task is None:
            return

        task.status = TaskStatus.FAILED

        update_task(db, task)

        dead_letter_queue.enqueue(task.id,task.priority)

    except Exception as e:
        print(f"Unexpected Error: {e}")

        task = get_task_for_worker(db, task_id)

        if task is None:
            return

        task.status = TaskStatus.FAILED

        update_task(db, task)
    
    
    
    