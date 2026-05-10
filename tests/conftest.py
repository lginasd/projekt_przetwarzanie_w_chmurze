import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import DataBase

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture
def db():
    DataBase.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()

    DataBase.metadata.drop_all(bind=engine)
