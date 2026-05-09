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
    return get_user(db, user_id)

@router.post("/")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user.email, user.hashed_password, user.is_admin)
