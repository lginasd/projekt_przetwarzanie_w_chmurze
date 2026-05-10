from decimal import Decimal

from app.services.product import create_product


def test_create_product(db):
    product = create_product(
        db,
        "Laptop",
        Decimal("999.99"),
        5
    )

    assert product is not None
    assert product.id is not None
    assert product.name == "Laptop"
    assert product.quantity == 5
