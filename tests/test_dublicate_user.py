from fastapi import HTTPException
import pytest

from app.services.user import create_user


def test_create_duplicate_user_returns_none(db):
    create_user(
        db,
        "test@example.com",
        "password123"
    )

    with pytest.raises(HTTPException) as exc:
        create_user(
            db,
            "test@example.com",
            "password123"
        )

    assert exc.value.status_code == 409
