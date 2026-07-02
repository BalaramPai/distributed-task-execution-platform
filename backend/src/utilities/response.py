# src/utilities/response.py

from fastapi.encoders import jsonable_encoder

from fastapi.responses import JSONResponse


def success_response(
    message: str,
    data=None,
    status_code: int = 200
):

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            "status": True,
            "data": data,
            "message": message,
            "error": None
        }),
    )


def error_response(
    message: str,
    error=None,
    status_code: int = 400
):

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
    {
        "status": False,
        "data": [],
        "message": message,
        "error": error,
    }
),
    )