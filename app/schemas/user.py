from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str = Field(min_length=8)
    is_admin: bool = False
