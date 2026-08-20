# src/main.py

from fastapi import FastAPI
from src.routes.healthRoutes import router as health_router
from src.routes.taskRoutes import router as tasks_router
from src.routes.authRoutes import router as auth_router
from src.routes.schedulerRoutes import router as scheduler_router
from src.routes.dependencyRoutes import router as dependency_router
from src.workers.workerManager import (
    start_workers,
    shutdown_workers
)
from src.service.recoveryService import recover_tasks
from src.constants.workerConstants import NUM_WORKERS

from contextlib import asynccontextmanager

# So we create a thread for the worker process so that the worker and FASTAPI share the same process but work on mutliple threads sharing the same resources.
@asynccontextmanager
async def lifespan(app: FastAPI): 
    
    # Recover unfinished tasks and rebuild the runtime heap before workers begin consuming tasks.
    recover_tasks()
    
    # Start the worker threads.
    print("Starting Worker Threads.")  
    start_workers(NUM_WORKERS)      # We start to worker threads here but hide the execution in the manager along with other functionalities necessary for scheduling.
    
    yield       # A yielding thread does not go into a sleeping or blocked state. It simply moves from the Running state back to the Runnable state, making it eligible to be scheduled again immediately
    
    # Gracefully shut down all workers when the FastAPI application stops.
    # Workers finish their current tasks before their threads are joined.
    shutdown_workers()
    
app = FastAPI(title="Distributed Task Execution Platform",version="1.0.0",lifespan=lifespan) # We include the thread here inside the FastAPI Process.


app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(scheduler_router)
app.include_router(dependency_router)