from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.auth import get_current_admin
from app.services.product import get_products, get_product, create_product, delete_product, update_product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "/",
    status_code=200,
    response_model=list[ProductResponse]
)
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.get(
    "/{product_id}",
    status_code=200,
    response_model=ProductResponse,
    responses={
        404: {
            "description": "Product not found"
        }
    }
)
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
    status_code=201,
    responses={
        401: {
            "description": "Unauthorised"
        },
        403: {
            "description": "Permission denied"
        },
        409: {
            "description": "Product already exists"
        }
    }
)
def add_product(
    product: ProductCreate,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return create_product(
        db,
        product.name,
        product.price,
        product.quantity
    )


@router.put(
    "/{product_id}",
    status_code=200,
    response_model=ProductResponse,
    responses={
        401: {
            "description": "Unauthorised"
        },
        403: {
            "description": "Permission denied"
        },
        404: {
            "description": "Product not found"
        }
    }
)
def edit_product(
    product_id: int,
    updated_product: ProductUpdate,
    _: User = Depends(get_current_admin),
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
    status_code=200,
    response_model=ProductResponse,
    responses={
        401: {
            "description": "Unauthorised"
        },
        403: {
            "description": "Permission denied"
        },
        404: {
            "description": "Product not found"
        },
        409: {
            "description": "Product is contained in one or many orders"
        },
    }
)
def remove_product(
    product_id: int,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return delete_product(db, product_id)
