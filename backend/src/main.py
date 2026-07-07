# src/main.py

from fastapi import FastAPI
from src.routes.healthRoutes import router as health_router
from src.routes.taskRoutes import router as tasks_router
from src.routes.authRoutes import router as auth_router

from src.workers.taskWorker import worker

import threading
from contextlib import asynccontextmanager

# So we create a thread for the worker process so that the worker and FASTAPI share the same process but work on mutliple threads sharing the same resources.
@asynccontextmanager
async def lifespan(app: FastAPI):   
    print("Starting Worker Thread.")
    worker_thread = threading.Thread(target=worker,daemon=True)
    worker_thread.start()
    yield
    
    
app = FastAPI(title="Distributed Task Execution Platform",version="1.0.0",lifespan=lifespan) # We include the thread here inside the FastAPI Process.


app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(auth_router)