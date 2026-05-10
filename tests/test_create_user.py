from app.services.user import create_user


def test_create_user(db):
    user = create_user(
        db,
        "test@example.com",
        "password123"
    )

    assert user is not None
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_admin is False
