from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import DataBase

if TYPE_CHECKING:
    from app.models.order import Order

class User(DataBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )

    is_admin: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )


    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"
    )
