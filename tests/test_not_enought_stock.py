from decimal import Decimal

import pytest

from fastapi import HTTPException

from app.services.order import create_order
from app.services.product import create_product
from app.services.user import create_user
from app.schemas.order import OrderItemCreate


def test_create_order_with_not_enough_stock(db):
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
        1
    )

    assert product is not None

    with pytest.raises(HTTPException) as exc:
        create_order(
            db,
            user.id,
            [
                OrderItemCreate(
                    product_id=product.id,
                    quantity=5
                )
            ]
        )

    assert exc.value.status_code == 400
