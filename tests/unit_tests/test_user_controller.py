import pytest

from models.user import User
from controllers.user_controller import UserController
from repository.user_repository import UserManager
from models.auth import Auth
from models.permission import role_required


@pytest.fixture
def mock_authenticated_user(mocker):
    """Fixture to mock an authenticated user."""
    fake_payload = {"sub": 1, "role": "Management"}
    mocker.patch.object(Auth, "is_authenticated", return_value=fake_payload)
    return fake_payload


def test_create_user_success(
    mock_authenticated_user,
    mock_session,
    capsys,
    mocker
):
    """Check an user has been created and displayed."""
    mocker.patch("models.permission.role_required",
                 lambda *roles: lambda f: f)
    mocker.patch.object(UserManager, 'save')

    UserController.create_user(
        mock_session, "Bob", "bob@example.com", "securepassword", "Sales"
    )

    captured = capsys.readouterr()
    assert "User created successfully" in captured.out


def test_get_user_existing(
    mock_authenticated_user,
    mock_session,
    capsys,
    mocker
):
    """Test retrieving an existing user."""
    fake_user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    mocker.patch.object(UserManager, 'get_user_by_id', return_value=fake_user)

    UserController.get_user(mock_session, 1)

    captured = capsys.readouterr()
    assert "User found" in captured.out


def test_login_user_success(mock_session, capsys, mocker):
    """Test successful login."""
    user = User(id=1, name="Alice", email="alice@example.com", role="Sales")
    mocker.patch.object(Auth, "authenticate_user", return_value={
        "user": user,
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token"
    })
    mocker.patch.object(Auth, "save_token")

    UserController.login_user(mock_session, "alice@example.com", "mypassword")

    captured = capsys.readouterr()
    assert "Connected! Welcome, Alice." in captured.out


def test_login_user_failure(mock_session, capsys, mocker):
    """Test login failure due to incorrect credentials."""
    mocker.patch.object(Auth, "authenticate_user", return_value=None)

    UserController.login_user(
        mock_session,
        "alice@example.com",
        "wrongpassword"
    )

    captured = capsys.readouterr()
    assert "Incorrect email or password." in captured.out
