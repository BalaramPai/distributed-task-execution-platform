# src/service/authService.py

from sqlalchemy.orm import Session

from src.dao.authDao import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_id
)

from fastapi.security import OAuth2PasswordRequestForm

from src.models.userModel import User

from src.schemas.authSchema import (
    RegisterSchema,
    UserResponseSchema,
    LoginResponseSchema
)

from src.utilities.password import (
    hash_password,
    verify_password
)

from src.utilities.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token
)

from src.exceptions.authExceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    InvalidCredentialsException,
    InvalidTokenException
)


def register_service(
    db: Session,
    register_data: RegisterSchema
):

    if get_user_by_email(db, register_data.email):

        raise DuplicateEmailException(
            "Email already registered."
        )

    if get_user_by_username(
        db,
        register_data.username
    ):

        raise DuplicateUsernameException(
            "Username already exists."
        )


    hashed_password = hash_password(
        register_data.password
    )

    user = User(
        username=register_data.username,
        email=register_data.email,
        password_hash=hashed_password
    )

    saved_user = create_user(
        db,
        user
    )

    return UserResponseSchema(
        id=saved_user.id,
        username=saved_user.username,
        email=saved_user.email,
        role=saved_user.role,
        createdAt=saved_user.created_at
    )


def login_service(
    db: Session,
    form_data: OAuth2PasswordRequestForm
):

    user = get_user_by_email(
        db,
        form_data.username
    )

    if user is None:

        raise InvalidCredentialsException(
            "Invalid email or password."
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):

        raise InvalidCredentialsException(
            "Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    refresh_token = create_refresh_token(
    {
        "sub": str(user.id),
        "role": user.role
    }
)

    return LoginResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )


def refresh_token_service(
    token: str
):

    payload = verify_token(token)

    if payload is None:

        raise InvalidTokenException(
            "Invalid refresh token."
        )

    if payload.get("type") != "refresh":

        raise InvalidTokenException(
            "Invalid refresh token."
        )

    access_token = create_access_token(
    {
        "sub": payload["sub"],
        "role": payload["role"]
    }
    )

    return LoginResponseSchema(
        access_token=access_token,
        refresh_token=token
    )


def get_current_user_service(
    db: Session,
    token: str
):

    payload = verify_token(token)

    if payload is None:

        raise InvalidTokenException(
            "Invalid token."
        )

    if payload.get("type") != "access":

        raise InvalidTokenException(
            "Invalid access token."
        )

    user = get_user_by_id(
        db,
        int(payload["sub"])
    )

    if user is None:

        raise InvalidTokenException(
            "User not found."
        )

    return user


def logout_service():

    return {
        "message": "Logged out successfully."
    }