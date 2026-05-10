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
    if new_email is None and new_password is None:
        raise HTTPException(
            status_code=422,
            detail="No changes supplied"
        )

    user = get_user(db, user_id)

    if user is None:
        return None

    if new_email:
        user.email = new_email
    if new_password:
        user.hashed_password = hash_password(new_password)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

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

    if new_email is None and new_password is None and new_is_admin is None:
        raise HTTPException(
            status_code=422,
            detail="No changes supplied"
        )

    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if new_is_admin is not None and user == current_user:
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

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

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

    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    db.delete(user)
    db.commit()

    return user
