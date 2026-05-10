from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0, default=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    quantity: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str
    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0, default=0)
