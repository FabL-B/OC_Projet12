from models.user import User
from controllers.user_controller import UserController
from models.user_manager import UserManager


def test_create_user_success(mock_session, capsys, mocker):
    """Check an user has been created and displayed."""
    mocker.patch.object(
        UserManager,
        'save',
        return_value=User(
            id=1,
            name="Bob",
            email="bob@example.com",
            role="Sales"
        )
    )

    UserController.create_user(
        mock_session, "Bob",
        "bob@example.com",
        "securepassword",
        "Sales"
    )

    captured = capsys.readouterr()
    assert "User created successfully" in captured.out


def test_get_user_existing(mock_session, capsys, mocker):
    """Test retrieving an existing user."""
    fake_user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    mocker.patch.object(UserManager, 'get_user_by_id', return_value=fake_user)

    UserController.get_user(mock_session, 1)

    captured = capsys.readouterr()
    assert "User found" in captured.out
