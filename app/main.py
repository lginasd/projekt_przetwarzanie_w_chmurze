from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.database import engine, DataBase
from app.routers import auth, order, product, user

# Must be imported even if unused to create according database tables
from app.models.product import Product
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem


app = FastAPI(
    title="e-commerce API"
)


DataBase.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(order.router)
app.include_router(product.router)
app.include_router(user.router)

@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
