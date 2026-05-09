from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database import DataBase

class Product(DataBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )
