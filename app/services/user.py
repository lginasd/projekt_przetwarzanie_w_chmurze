from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.utils.security import hash_password


def create_user(
    db: Session,
    email: str,
    password: str,
):
    hashed_password = hash_password(password)

    user = User(
        email=email,
        hashed_password=hashed_password,
        is_admin=False
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return None

    return user


def get_users(
    db: Session,
):
    return db.query(User).all()


def get_user(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def update_me(
    db: Session,
    user_id: int,
    new_email: str|None,
    new_password: str|None,
):
    if not (new_email or new_password):
        raise HTTPException(
            status_code=401,
            detail="No changes supplied"
        )

    user = get_user(db, user_id)

    if user is None:
        return None

    if new_email:
        user.email = new_email
    if new_password:
        user.hashed_password = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user_id: int,
    current_user: User,
    new_email: str|None,
    new_password: str|None,
    new_is_admin: bool|None,
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    if not (new_email or new_password or new_is_admin):
        raise HTTPException(
            status_code=422,
            detail="No changes supplied"
        )

    user = get_user(db, user_id)

    if user is None:
        return None

    if new_is_admin and user == current_user:
        raise HTTPException(
            status_code=422,
            detail="Changing own status is not allowed"
        )

    if new_email:
        user.email = new_email
    if new_password:
        user.hashed_password = hash_password(new_password)
    if new_is_admin:
        user.is_admin = new_is_admin

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user_id: int,
    current_user: User,
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404
                )
