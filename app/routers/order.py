from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.schemas.order import OrderCreate, OrderPatchStatus, OrderResponse
from app.services.auth import get_current_admin, get_current_user
from app.services.order import change_order_status, create_order, get_order, get_orders, get_user_orders, delete_order


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
            "description": "Unauthorized"
        },
        403: {
            "description": "Permission denied"
        },
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
            "description": "Unauthorized"
        },
        403: {
            "description": "Access denied"
        },
        404: {
            "description": "Order does not exist"
        }
    }
)
def read_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = get_order(
        db,
        order_id,
        current_user
    )

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
            "description": "Unauthorized"
        },
        403: {
            "description": "Access denied"
        },
    }
)
def place_order(
    order_items: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_order(
        db,
        current_user.id,
        order_items.items
    )


@router.patch(
    "/{order_id}",
    status_code=200,
    response_model=OrderResponse,
    responses={
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Access denied"
        },
        404: {
            "description": "Order not found"
        }
    }
)
def patch_order_status(
    order_id: int,
    order_status: OrderPatchStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return change_order_status(
        db,
        order_id,
        order_status.status,
        current_user
    )


@router.delete(
    "/{order_id}",
    status_code=200,
    response_model=OrderResponse,
    responses={
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Permission denied"
        },
        404: {
            "description": "Order not found"
        },
        422: {
            "description": "Validation error"
        }
    },
)
def remove_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return delete_order(
        db,
        order_id
    )
