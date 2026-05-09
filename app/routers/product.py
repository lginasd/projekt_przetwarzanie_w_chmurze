from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.product import get_products, get_product, create_product
from app.schemas.product import ProductCreate


router = APIRouter()


@router.get("/products")
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get("/product/{id}")
def read_product(
    id: int,
    db: Session = Depends(get_db)
):
    return get_product(db, id)


@router.post("/product")
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product.name, product.price)
