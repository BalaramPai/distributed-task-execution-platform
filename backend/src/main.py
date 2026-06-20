# src/main.py

from fastapi import FastAPI
from src.routes.healthRoutes import router as health_router
from src.routes.taskRoutes import router as tasks_router

app = FastAPI(title="Distributed Task Execution Platform",version="1.0.0")

app.include_router(health_router)
app.include_router(tasks_router)