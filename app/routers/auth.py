from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import TokenResponse
from app.services.auth import login_and_give_token


router = APIRouter(
    prefix="/auth",
    tags=["Users", "Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=200,
    responses={
        401: {
            "description": "Invalid credentials"
        },
        422: {
            "description": "Validation error"
        }
    }
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_and_give_token(form_data, db)
