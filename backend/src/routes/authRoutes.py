# src/routes/authRoutes.py

from fastapi import (
    APIRouter,
    Depends
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from src.database.database import get_db

from src.schemas.authSchema import (
    RegisterSchema,
    RefreshTokenSchema
)

from src.controllers.authController import (
    register_controller,
    login_controller,
    refresh_token_controller
)

from src.controllers.authController import (
    logout_controller
)

from src.dependencies.auth import get_current_user

router = APIRouter(tags=["Authentication & Authorization"])


@router.post("/auth/register")
def register(
    register_data: RegisterSchema,
    db: Session = Depends(get_db)
):

    return register_controller(
        db,
        register_data
    )


@router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_controller(
        db,
        form_data
    )


@router.post("/auth/refresh")
def refresh_token(
    refresh_data: RefreshTokenSchema
):

    return refresh_token_controller(
        refresh_data
    )
    
@router.post("/auth/logout")
def logout(

    current_user=Depends(get_current_user)

):

    return logout_controller()