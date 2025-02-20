from app.models.user import User


def test_create_user(session_test):
    user = User(
        id=1,
        name="Test User",
        email="test@mail.com",
        role="Sales"
    )
    user.set_password("password")
    session_test.add(user)
    session_test.commit()
    retrieved_user = session_test.query(User).filter_by(
        email="test@mail.com").first()
    assert retrieved_user is not None
    assert retrieved_user.name == "Test User"
    assert retrieved_user.verify_password("password") is True


def test_get_user_by_id(session_test):
    user = User(id=2, name="User2", email="user2@mail.com", role="Sales")
    user.set_password("user2pass")
    session_test.add(user)
    session_test.commit()
    retrieved_user = session_test.get(User, 2)
    assert retrieved_user is not None
    assert retrieved_user.email == "user2@mail.com"
    assert retrieved_user.verify_password("user2pass") is True


def test_delete_user(session_test):
    user = User(id=3, name="To Delete", email="delete@mail.com", role="Sales")
    user.set_password("deletepass")
    session_test.add(user)
    session_test.commit()
    session_test.delete(user)
    session_test.commit()
    assert session_test.get(User, 3) is None
