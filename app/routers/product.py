from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product import get_products, get_product, create_product, delete_product, update_product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get("/{product_id}")
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)

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


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def edit_product(
    product_id: int,
    updated_product: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = update_product(
        db,
        product_id,
        updated_product.name,
        updated_product.price
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.delete(
    "/{product_id}",
    status_code=204
)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    removed = delete_product(db, product_id)
    if removed is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return None

