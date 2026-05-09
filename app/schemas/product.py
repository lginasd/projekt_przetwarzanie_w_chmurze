from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str
    price: float = Field(gt=0)
