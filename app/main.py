from fastapi import FastAPI

from app.database import engine, Base
from app.routers import product


app = FastAPI(
    title="e-commerce API"
)


Base.metadata.create_all(bind=engine)

app.include_router(product.router)

# TODO: @app.exception_handler(...)
