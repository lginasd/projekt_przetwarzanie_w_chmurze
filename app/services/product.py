from sqlalchemy.orm import Session

from app.models.product import Product


def create_product(
    db: Session,
    name: str,
    price: float,
    quantity: int
):
    product = Product(
        name=name,
        price=price,
        quantity=quantity
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session):
    return db.query(Product).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def update_product(
    db: Session,
    product_id: int,
    name: str,
    price: float
):
    product = get_product(db, product_id)

    if product is None:
        return None

    product.name = name
    product.price = price

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product is None:
        return None

    db.delete(product)
    db.commit()

    return product
