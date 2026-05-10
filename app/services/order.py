from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from app.models.user import User
from app.schemas.order import OrderItemCreate, OrderResponse
from app.services.product import get_product


def create_order(
    db: Session,
    user_id: int,
    items: list[OrderItemCreate]
):
    for item in items:
        product = get_product(db, item.product_id)

        if product is None:
            raise HTTPException(
                status_code=400,
                detail="Product does not exist"
            )

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )

    order = Order(user_id=user_id)

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in items:
        product = get_product(db, item.product_id)

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        if product is None:
            raise ValueError("Product was removed after checking")

        product.quantity -= item.quantity

        db.add(order_item)
        db.flush()

    # TODO
    # 1. calculate total

    db.commit()

    return order


def get_orders(db: Session):
    return db.query(Order).all()


def get_user_orders(db: Session, current_user: User):
    return db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()


def get_order(
    db: Session,
    order_id: int,
    current_user: User
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if order is None:
        return None

    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return order


def change_order_status(
    db: Session,
    order_id: int,
    order_status: OrderStatus,
    current_user: User
):
    order = get_order(db, order_id, current_user)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if not order.status == OrderStatus.PENDING:
        raise HTTPException(
            status_code=422,
            detail="Operation is not permitted with current order status"
        )

    order.status = order_status

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def delete_order(
    db: Session,
    order_id: int,
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return order
