from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserRsponse(BaseModel):
    email: str
    is_admin: bool

    class Config:
        from_attributes = True
