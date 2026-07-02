# src/utilities/response.py

from fastapi.responses import JSONResponse


def success_response(
    message: str,
    data=None,
    status_code: int = 200
):

    return JSONResponse(
        status_code=status_code,
        content={
            "status": True,
            "data": data,
            "message": message,
            "error": None
        },
    )


def error_response(
    message: str,
    error=None,
    status_code: int = 400
):

    return JSONResponse(
        status_code=status_code,
        content={
            "status": False,
            "data": [],
            "message": message,
            "error": error
        },
    )