from fastapi import FastAPI

from app.database import engine, DataBase
from app.routers import product

# Must be imported even if unused to create according database tables
from app.models.product import Product
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem


app = FastAPI(
    title="e-commerce API"
)


DataBase.metadata.create_all(bind=engine)

app.include_router(product.router)

# TODO: @app.exception_handler(...)
