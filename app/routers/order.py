from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.order import OrderCreate, OrderResponse
from app.services.order import create_order, get_order, get_orders


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/")
def read_orders(
    db: Session = Depends(get_db),
):
    return get_orders(db)

@router.get("/{order_id}")
def read_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return get_order(db, order_id)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201
)
def place_order(
    order_items: OrderCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    return create_order(db, user_id, order_items.items)
