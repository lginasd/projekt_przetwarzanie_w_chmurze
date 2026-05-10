from decimal import Decimal

from app.services.order import create_order
from app.services.product import create_product
from app.services.user import create_user
from app.schemas.order import OrderItemCreate


def test_create_order_reduces_stock(db):
    user = create_user(
        db,
        "test@example.com",
        "password123"
    )

    assert user is not None

    product = create_product(
        db,
        "Laptop",
        Decimal("1000"),
        10
    )

    assert product is not None

    order = create_order(
        db,
        user.id,
        [
            OrderItemCreate(
                product_id=product.id,
                quantity=3
            )
        ]
    )

    assert order is not None
    assert order.id is not None

    db.refresh(product)

    assert product.quantity == 7
