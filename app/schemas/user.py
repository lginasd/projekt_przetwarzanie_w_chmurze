from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


PasswordStr = Annotated[
    str,
    Field(
        min_length=8,
        examples=["secure_p4ssw0rd"]
    )
]

class UserRegister(BaseModel):
    email: EmailStr = Field(examples=[
        "user@example.com",
        "admin@internal.org"
    ])
    password: PasswordStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: EmailStr
    password: PasswordStr
    is_admin: bool = Field(default=False)


class UserPatch(BaseModel):
    new_email: EmailStr|None = None
    new_password: str|None = Field(
        default=None,
        min_length=8,
        examples=["new_secure_p4ssw0rd"]
    )
