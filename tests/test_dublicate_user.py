from app.services.user import create_user


def test_create_duplicate_user_returns_none(db):
    create_user(
        db,
        "test@example.com",
        "password123"
    )

    user = create_user(
        db,
        "test@example.com",
        "password123"
    )

    assert user is None
