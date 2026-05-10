from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import DataBase


class OrderItem(DataBase):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )


    order: Mapped[int] = relationship(
        back_populates="items"
    )

    product: Mapped[int] = relationship(
        "Product",
        back_populates="order_items"
    )
