from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.schemas.user import UserRegister, UserRsponse
from app.services.auth import get_current_user, get_current_admin
from app.services.user import create_user, get_user, get_users


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    status_code=201,
    response_model=UserRsponse,
    responses={
        409: {
            "description": "User is already registered"
        }
    }
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    user = create_user(db, user.email, user.password)

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="User is already registered"
        )

    return user


@router.get(
    "/",
    status_code=200,
    response_model=list[UserRsponse],
    responses={
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Permission denied"
            }
        }
)
def read_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return get_users(db)


@router.get(
    "/me",
    status_code=200,
    response_model=UserRsponse,
    responses={
        401: {
            "description": "Unauthorized"
        }
    }
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get(
    "/{user_id}",
    status_code=200,
    response_model=UserRsponse,
    responses={
        401: {
            "description": "Unauthorized"
        },
        403: {
            "description": "Permission denied"
        },
        404: {
            "description": "User not found"
        },
    }
)
def read_user(
    user_id: int,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
