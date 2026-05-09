from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.product import ProductCreate, ProductResponse
from app.services.product import get_products, get_product, create_product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get("/{id}")
def read_product(
    id: int,
    db: Session = Depends(get_db)
):
    product = get_product(db, id)

    if not product:
        raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
    
    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(
        db,
        product.name,
        product.price
    )

# TODO: put_product, delete_product
