from sqlalchemy.orm import Session

from app.models.product import Product


def create_product(db: Session, name: str, price: float):
    product = Product(
        name=name,
        price=price
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
