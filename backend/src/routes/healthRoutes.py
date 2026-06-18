# src/routes/healthRoutes.py

from fastapi import APIRouter
from src.utilities.response import success_response,error_response


router = APIRouter()

@router.get("/health")
def health():
    try:
        return success_response(message="Server is Up and Running")
    except Exception as e:
        return error_response(message="Server is down.",error=str(e))
        
