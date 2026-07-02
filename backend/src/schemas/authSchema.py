# src/schemas/authSchema.py

import re

from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


class RegisterSchema(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=20
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=64
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one digit."
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]",
            value
        ):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value




class RefreshTokenSchema(BaseModel):
    refresh_token: str


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    createdAt: datetime


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"