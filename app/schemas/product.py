from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0, default=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str
    price: float = Field(gt=0)
