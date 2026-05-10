from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.auth import get_current_user
from app.services.order import create_order, get_order, get_orders, get_user_orders


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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.is_admin:
        return get_orders(db)
    else:
        return get_user_orders(db, current_user)

@router.get(
    "/{order_id}",
    status_code=200,
    response_model=OrderResponse,
    responses= {
        401: {
            "detail": "Unauthorized"
        },
        404: {
            "detail": "Order does not exist"
        }
    }
)
def read_order(
    order_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = get_order(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order does not exist"
        )

    return order



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
    current_user: User = Depends(get_current_user),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_order(
        db,
        current_user.id,
        order_items.items
    )
