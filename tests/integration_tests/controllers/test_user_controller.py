from app.controllers.user_controller import UserController
from app.models.user import User


def test_create_user_success(session, mocker):
    """
    Tests successful creation of a user.
    """
    user_payload = {"id": 99, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    user_data = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "securepassword",
        "role": "Support"
    }
    mocker.patch(
        "app.views.user_view.UserView.get_user_creation_data",
        return_value=user_data
    )

    controller = UserController()
    controller.create_user(session=session)

    created_user = session.query(User).filter_by(
        email="newuser@example.com").first()
    assert created_user is not None
    assert created_user.name == "New User"
    assert created_user.role == "Support"


def test_update_user_success(session, mocker, create_users):
    """
    Tests successful update of a user.
    """
    sales_user, _ = create_users

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    mocker.patch(
        "app.views.user_view.UserView.get_user_update_data",
        return_value={
            "name": "Updated Name",
            "email": "updated@example.com"
        }
    )

    controller = UserController()
    controller.update_user(session=session, user_id=sales_user.id)

    updated_user = session.get(User, sales_user.id)
    assert updated_user.name == "Updated Name"
    assert updated_user.email == "updated@example.com"


def test_delete_user_success(session, mocker, create_users):
    """
    Tests successful deletion of a user.
    """
    sales_user, _ = create_users

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)
    mocker.patch(
        "app.views.user_view.UserView.confirm_deletion",
        return_value=True
    )

    controller = UserController()
    controller.delete_user(session=session, user_id=sales_user.id)

    assert session.get(User, sales_user.id) is None
