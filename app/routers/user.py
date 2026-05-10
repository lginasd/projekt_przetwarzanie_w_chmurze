from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user import UserCreate
from app.services.user import create_user, get_user, get_users


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserCreate,
    status_code=201
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    user = create_user(db, user.email, user.password)

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="User is already registered"
        )

    return user


@router.get("/")
def read_users(
    db: Session = Depends(get_db)
):
    return get_users(db)


@router.get("/{user_id}")
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
