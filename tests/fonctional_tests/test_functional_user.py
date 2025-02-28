import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from app.controllers.app_controller import AppController
from app.controllers.user_controller import UserController
from app.auth.auth import Auth
from config.database import Base
from app.models.user import User
from app.views.user_view import UserView
import builtins

test_engine = create_engine(
    "postgresql://test_user:test_password@localhost:5432/epicevent_test_db"
)
TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture(scope="function")
def session_test():
    """Creates a temporary PostgreSQL database for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def app_controller(session_test):
    """Initializes AppController with a test session."""
    return AppController(session_test)


@pytest.fixture(scope="function")
def user_controller(session_test):
    """Initializes UserController with a test session."""
    return UserController()


@pytest.fixture(scope="function")
def authenticated_users(session_test):
    """
    Creates and authenticates three users (Sales, Management, Support)
    with real tokens.
    """
    users = [
        {
            "name": "Sales User",
            "email": "sales@example.com",
            "role": "Sales",
            "password": "salespassword",
        },
        {
            "name": "Management User",
            "email": "management@example.com",
            "role": "Management",
            "password": "managementpassword",
        },
        {
            "name": "Support User",
            "email": "support@example.com",
            "role": "Support",
            "password": "supportpassword",
        },
    ]
    tokens = {}
    for user_data in users:
        existing_user = session_test.query(User).filter_by(
            email=user_data["email"]
        ).first()
        if existing_user:
            session_test.delete(existing_user)
            session_test.commit()

        user = User(
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"],
        )
        user.set_password(user_data["password"])
        session_test.add(user)
        session_test.commit()

        auth_response = Auth.authenticate_user(
            session_test, user.email, user_data["password"]
        )
        tokens[user_data["role"]] = auth_response["access_token"]

    return tokens


@pytest.fixture(autouse=True)
def mock_auth(authenticated_users):
    """Mocks Auth.is_authenticated() to return expected user payloads."""
    def fake_is_authenticated():
        token, _ = Auth.load_token()
        for role, access_token in authenticated_users.items():
            if token == access_token:
                return {"id": "1", "name": f"{role} User", "role": role}
        return None

    with patch(
        "app.auth.auth.Auth.is_authenticated",
        side_effect=fake_is_authenticated
    ):
        yield


def test_create_user(user_controller, session_test, authenticated_users):
    """Tests user creation functionality with Management role."""
    user_data = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "newpassword",
        "role": "Sales",
    }

    Auth.save_token(authenticated_users["Management"], "")

    with patch.object(
        UserView, "get_user_creation_data", return_value=user_data
    ):
        user_controller.create_user(session_test)

    user = session_test.query(User).filter_by(
        email="newuser@example.com").first()
    assert user is not None
    assert user.name == "New User"
    assert user.role == "Sales"


def test_update_user(user_controller, session_test, authenticated_users):
    """Tests user update functionality with Management role."""
    user = User(name="Old User", email="olduser@example.com", role="Sales")
    user.set_password("oldpassword")
    session_test.add(user)
    session_test.commit()

    updated_data = {"name": "Updated User", "role": "Support"}

    Auth.save_token(authenticated_users["Management"], "")

    with patch.object(
        UserView, "get_user_update_data", return_value=updated_data
    ):
        user_controller.update_user(session_test, user.id)

    updated_user = session_test.query(User).filter_by(id=user.id).first()
    assert updated_user.name == "Updated User"
    assert updated_user.role == "Support"


def test_delete_user(user_controller, session_test, authenticated_users):
    """Tests user deletion functionality with Management role."""
    user = User(
        name="Delete User", email="deleteuser@example.com", role="Sales"
    )
    user.set_password("deletepassword")
    session_test.add(user)
    session_test.commit()

    Auth.save_token(authenticated_users["Management"], "")

    with patch.object(builtins, "input", lambda _: "y"):
        user_controller.delete_user(session_test, user.id)

    deleted_user = session_test.query(User).filter_by(id=user.id).first()
    assert deleted_user is None
