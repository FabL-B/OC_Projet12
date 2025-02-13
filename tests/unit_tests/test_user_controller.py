import pytest
from models.user import User
from controllers.user_controller import UserController
from services.user_service import UserService
from models.auth import Auth


@pytest.fixture
def user_controller():
    """Fixture to instantiate UserController."""
    return UserController()


def test_list_all_users(mocker, user_controller, mock_session):
    """Test retrieving all users."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        UserService,
        "list_all",
        return_value=[
            User(id=1, name="Bob"),
            User(id=2, name="Alice"),
        ],
    )

    users = user_controller.list_all(mock_session)

    assert len(users) == 2
    assert users[0].name == "Bob"
    assert users[1].name == "Alice"
    UserService.list_all.assert_called_once_with(mock_session)


def test_get_user(mocker, user_controller, mock_session):
    """Test retrieving a specific user."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        UserService,
        "get_by_id",
        return_value=User(id=1, name="Bob"),
    )

    user = user_controller.get(mock_session, entity_id=1)

    assert user.name == "Bob"
    UserService.get_by_id.assert_called_once_with(mock_session, 1)


def test_create_user(mocker, user_controller, mock_session):
    """Test creating a user."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        UserService,
        "create",
        return_value=User(id=1, name="Bob", email="bob@example.com"),
    )

    user_controller.create(
        mock_session,
        name="Bob",
        email="bob@example.com",
        password="securepassword",
        role="Sales",
    )

    UserService.create.assert_called_once_with(
        mock_session,
        name="Bob",
        email="bob@example.com",
        password="securepassword",
        role="Sales",
    )


def test_update_user(mocker, user_controller, mock_session):
    """Test updating a user."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(UserService, "update", return_value=True)

    success = user_controller.update(
        mock_session, entity_id=1, data={"name": "Bob Updated"}
    )

    assert success is True
    UserService.update.assert_called_once_with(
        mock_session, 1, {"name": "Bob Updated"}
    )


def test_delete_user(mocker, user_controller, mock_session):
    """Test deleting a user."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(UserService, "delete", return_value=True)

    success = user_controller.delete(mock_session, entity_id=1)

    assert success is True
    UserService.delete.assert_called_once_with(mock_session, 1)
