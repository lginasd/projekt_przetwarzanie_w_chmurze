from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    is_admin: bool = Field(default=False)


class UserPatch(BaseModel):
    new_email: EmailStr|None = None
    new_password: str|None = Field(default=None, min_length=8)
