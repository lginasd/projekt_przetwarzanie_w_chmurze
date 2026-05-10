from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import DataBase

if TYPE_CHECKING:
    from app.models.order_item import OrderItem

class Product(DataBase):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )


    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product"
    )
