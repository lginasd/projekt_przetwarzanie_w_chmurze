from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import SECRET_KEY

from app.models.user import User
from app.utils.security import create_access_token, verify_password

from app.utils.security import (
    SECRET_KEY,
    ALGORITHM
)

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

credentials_exception = HTTPException(
    status_code=401,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def login_and_give_token(
    form_data: OAuth2PasswordRequestForm,
    db: Session
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if user is None:
        raise credentials_exception

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise credentials_exception

    token = create_access_token({
        "sub": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user


def get_current_admin(
    current_user: User = Depends(
        get_current_user
    )
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    return current_user
