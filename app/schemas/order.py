from pydantic import BaseModel, Field

from app.models.order_status import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: list[OrderItemCreate]
    status: OrderStatus

    class Config:
        from_attributes = True


class OrderPatchStatus(BaseModel):
    id: int
    status: OrderStatus

    class Config:
        from_attributes = True
