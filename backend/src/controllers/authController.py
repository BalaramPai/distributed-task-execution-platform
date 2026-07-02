# src/controllers/authController.py

from sqlalchemy.orm import Session

from src.schemas.authSchema import (
    RegisterSchema,
    RefreshTokenSchema
)

from src.service.authService import (
    register_service,
    login_service,
    refresh_token_service
)

from src.utilities.response import (
    success_response,
    error_response
)

from src.exceptions.authExceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    InvalidCredentialsException,
    InvalidTokenException
)

from src.service.authService import logout_service

from fastapi.security import OAuth2PasswordRequestForm


def register_controller(
    db: Session,
    register_data: RegisterSchema
):

    try:

        user = register_service(
            db,
            register_data
        )

        return success_response(
            message="User registered successfully.",
            data=user,
            status_code=201
        )

    except DuplicateEmailException as e:

        return error_response(
            message=str(e),
            status_code=409
        )

    except DuplicateUsernameException as e:

        return error_response(
            message=str(e),
            status_code=409
        )

    except Exception as e:

        return error_response(
            message="User registration failed.",
            error=str(e)
        )


def login_controller(
    db: Session,
    form_data: OAuth2PasswordRequestForm
):

    try:

        token = login_service(
            db,
            form_data
        )

        return token

    except InvalidCredentialsException as e:

        return error_response(
            message=str(e),
            status_code=401
        )

    except Exception as e:

        return error_response(
            message="Login failed.",
            error=str(e)
        )


def refresh_token_controller(
    refresh_data: RefreshTokenSchema
):

    try:

        token = refresh_token_service(
            refresh_data.refresh_token
        )

        return success_response(
            message="Token refreshed successfully.",
            data=token
        )

    except InvalidTokenException as e:

        return error_response(
            message=str(e),
            status_code=401
        )

    except Exception as e:

        return error_response(
            message="Token refresh failed.",
            error=str(e)
        )
        
def logout_controller():

    try:

        response = logout_service()

        return success_response(
            message=response["message"]
        )

    except Exception as e:

        return error_response(
            message="Logout failed.",
            error=str(e)
        )