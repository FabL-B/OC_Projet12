from models.user import User
from models.user_manager import UserManager


def test_save_user(mock_session):
    """Test to create an user and save it in database."""
    user = User(name="Bob", email="bob@example.com", role="Sales")
    user.set_password("securepassword")

    UserManager.save(mock_session, user)

    assert mock_session.add.called
    assert mock_session.commit.called


def test_get_user_by_id(mock_session):
    """Test a user with its ID."""
    user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    mock_session.get.return_value = user

    user = UserManager.get_user_by_id(mock_session, 1)

    assert user == user
    mock_session.get.assert_called_once_with(User, 1)


def test_authenticate_user_success(mock_session, mocker):
    """Test a correct connexion."""
    user = User(name="Alice", email="alice@example.com", role="Sales")
    user.set_password("mypassword")

    mocker.patch.object(UserManager, "get_user_by_email", return_value=user)

    result = UserManager.authenticate_user(
        mock_session,
        "alice@example.com",
        "mypassword"
    )
    assert result == user


def test_authenticate_user_wrong_password(mock_session, mocker):
    """Test an incorrect connexion (invalid password)."""
    user = User(name="Alice", email="alice@example.com", role="Sales")
    user.set_password("mypassword")

    mocker.patch.object(UserManager, "get_user_by_email", return_value=user)

    result = UserManager.authenticate_user(
        mock_session,
        "alice@example.com",
        "wrongpassword"
    )
    assert result is None
