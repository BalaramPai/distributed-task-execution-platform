# src/controller/dependencyController.py

from src.service.dependencyService import (
    get_task_dependencies_service,
    get_blocked_reason_service
)
from src.utilities.response import success_response, error_response


def get_task_dependencies_controller(db, task_id):
    try:
        dependency_response = get_task_dependencies_service(db, task_id)

        return success_response(
            message="Task dependencies retrieved successfully.",
            data=dependency_response
        )

    except Exception as e:
        return error_response(
            message="Failed to retrieve task dependencies.",
            error=str(e)
        )


def get_blocked_reason_controller(db, task_id):
    try:
        blocked_response = get_blocked_reason_service(db, task_id)

        return success_response(
            message="Blocked reason retrieved successfully.",
            data=blocked_response
        )

    except Exception as e:
        return error_response(
            message="Failed to retrieve blocked reason.",
            error=str(e)
        )