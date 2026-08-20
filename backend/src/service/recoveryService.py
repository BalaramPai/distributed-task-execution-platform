# src/service/recoveryService.py

from src.database.database import SessionLocal

from src.dao.taskDao import (
    get_in_progress_tasks,
    get_waiting_tasks,
    get_queued_tasks,
    update_task
)

from src.schemas.enums import TaskStatus

from src.service.dependencyService import (
    are_dependencies_completed
)

from src.queue.queueManager import task_queue


def recover_tasks():
    """
    Recovers task state when the application starts after a shutdown/crash.

    Recovery handles three cases:

    1. IN_PROGRESS tasks:
       These were being executed when the previous application stopped.
       They are reset to QUEUED.

    2. WAITING tasks:
       These depend on other tasks.
       If all their dependencies are now COMPLETED, they are changed to
       QUEUED. Otherwise, they remain WAITING.

    3. QUEUED tasks:
       These were already ready to execute before the application stopped.
       They are used to rebuild the runtime heap.

    After database recovery is complete, all QUEUED tasks are loaded
    into the runtime heap.
    """

    # Recovery is a startup operation rather than an HTTP request, so it creates and manages its own database session.
    db = SessionLocal()

    try:

        # ---------------------------------------------------------
        # 1. Recover interrupted IN_PROGRESS tasks
        # ---------------------------------------------------------

        # Find tasks that were being executed when the application stopped.
        in_progress_tasks = get_in_progress_tasks(db)

        for task in in_progress_tasks:

            # The previous worker could not finish this task.
            # Reset it so a worker can execute it again.
            task.status = TaskStatus.QUEUED

            # Persist the recovered state in PostgreSQL.
            update_task(db, task)

            # We will Rebuild the runtime heap by putting the task back into our existing TaskQueue once all recoveries are done at the end.


        # ---------------------------------------------------------
        # 2. Reconcile WAITING tasks
        # ---------------------------------------------------------

        # Find tasks that were waiting for dependencies when the previous application stopped.
        waiting_tasks = get_waiting_tasks(db)

        for task in waiting_tasks:

            # Check whether every dependency of this task has now reached COMPLETED status.
            if are_dependencies_completed(db, task.dependencies):

                # The task is no longer blocked, so make it executable.
                task.status = TaskStatus.QUEUED

                # Persist the new state.
                update_task(db, task)

            # We will Rebuild the runtime heap by putting the task back into our existing TaskQueue once all recoveries are done at the end.

        
        # ---------------------------------------------------------
        # 3. Recover interrupted QUEUED tasks.
        # ---------------------------------------------------------
        
        # Find tasks that were queued when the application stopped.
        in_queue_tasks = get_queued_tasks(db)

        for task in in_queue_tasks:
        
            # Rebuild the runtime heap by putting the task back into our existing TaskQueue.
            task_queue.enqueue(
                task.id,
                task.priority
            )
    finally:
        # Always close the recovery database session, even if recovery encounters an unexpected error.
        db.close()