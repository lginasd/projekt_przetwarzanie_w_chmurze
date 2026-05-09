from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    email: str,
    hashed_password: str,
    is_admin: bool
):
    user = User(
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin
    )

    db.add(user)
    db.commit()
    db.refresh(user)

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
