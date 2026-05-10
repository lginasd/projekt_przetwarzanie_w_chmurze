from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.auth import get_current_user
from app.services.order import create_order, get_order, get_orders


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get(
    "/",
    status_code=200,
    response_model=list[OrderResponse],
    responses= {
        401: {
            "detail": "Unauthorized"
        }
    }
)
def read_orders(
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_orders(db)

@router.get(
    "/{order_id}",
    status_code=200,
    response_model=list[OrderResponse],
    responses= {
        401: {
            "detail": "Unauthorized"
        }
    }
)
def read_order(
    order_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_order(db, order_id)


@router.post(
    "/",
    status_code=201,
    response_model=OrderResponse,
    responses={
        401: {
            "detail": "Unauthorized"
        }
    }
)
def place_order(
    order_items: OrderCreate,
    user_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_order(db, user_id, order_items.items)
