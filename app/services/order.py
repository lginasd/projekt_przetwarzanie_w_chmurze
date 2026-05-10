from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderItemCreate
from app.services.product import get_product


def create_order(
    db: Session,
    user_id: int,
    items: list[OrderItemCreate]
):
    order = Order(user_id=user_id)

    db.add(order)
    db.commit()
    db.refresh(order)

    # TODO
    # 1. check if product exists
    # 2. ensure that there is at least one product
    # 3. calculate total
    # 4. (maybe) apply discount

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

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(order_item)

    db.commit()

    return order


def get_orders(db: Session):
    return db.query(Order).all()


def get_order(
    db: Session,
    order_id: int
):
    return db.query(Order).filter(
        Order.id == order_id
    ).first()
