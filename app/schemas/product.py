from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
