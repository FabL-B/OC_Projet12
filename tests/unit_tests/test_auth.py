import jwt
import datetime
from models.auth import Auth
from models.user_manager import UserManager
from models.user import User


def test_create_access_token(mocker):
    """Test JWT access token generation."""
    mocker.patch("models.auth.JWT_SECRET", "fake_secret")
    mocker.patch("models.auth.JWT_ALGORITHM", "HS256")

    token = Auth.create_access_token(1, "Sales")
    payload = jwt.decode(token, "fake_secret", algorithms=["HS256"])

    assert payload["sub"] == "1"
    assert payload["role"] == "Sales"
    assert "exp" in payload


def test_create_refresh_token(mocker):
    """Test JWT refresh token generation."""
    mocker.patch("models.auth.JWT_SECRET", "fake_secret")
    mocker.patch("models.auth.JWT_ALGORITHM", "HS256")

    token = Auth.create_refresh_token(1)
    payload = jwt.decode(token, "fake_secret", algorithms=["HS256"])

    assert payload["sub"] == "1"
    assert "exp" in payload


def test_verify_token_valid(mocker):
    """Test if a JWT token is valid."""
    mocker.patch("models.auth.JWT_SECRET", "fake_secret")
    mocker.patch("models.auth.JWT_ALGORITHM", "HS256")

    token = Auth.create_access_token(1, "Sales")
    payload = Auth.verify_token(token)

    assert payload["sub"] == "1"
    assert payload["role"] == "Sales"


def test_verify_token_expired(mocker):
    """Test handling of an expire token."""
    mocker.patch("models.auth.JWT_SECRET", "fake_secret")
    mocker.patch("models.auth.JWT_ALGORITHM", "HS256")

    expired_time = datetime.datetime.now() - datetime.timedelta(seconds=1)
    expired_token = jwt.encode(
        {"sub": "1", "role": "Sales", "exp": expired_time.timestamp()},
        "fake_secret", algorithm="HS256"
    )
    assert Auth.verify_token(expired_token) == "expired"


def test_authenticate_user_success(mock_session, mocker):
    """Test successful authentification."""
    user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    user.verify_password = mocker.Mock(return_value=True)
    mock_session.get.return_value = user
    mocker.patch.object(UserManager, "get_user_by_email", return_value=user)
    mocker.patch.object(Auth, "create_access_token",
                        return_value="fake_access_token")
    mocker.patch.object(Auth, "create_refresh_token",
                        return_value="fake_refresh_token")

    result = Auth.authenticate_user(
        mock_session,
        "alice@example.com",
        "mypassword"
    )

    assert result is not None
    assert result["user"] == user
    assert result["access_token"] == "fake_access_token"
    assert result["refresh_token"] == "fake_refresh_token"


def test_save_and_load_token(mocker):
    """Test tokens save and load methods."""
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    Auth.save_token("access_token", "refresh_token")

    mock_file().write.assert_any_call("access_token\n")
    mock_file().write.assert_any_call("refresh_token")

    mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data="access_token\nrefresh_token")
    )
    access_token, refresh_token = Auth.load_token()

    assert access_token == "access_token"
    assert refresh_token == "refresh_token"


def test_is_authenticated_valid(mocker):
    """Test de la vérification d'une authentification réussie."""
    mocker.patch.object(
        Auth,
        "load_token",
        return_value=("valid_access_token", "valid_refresh_token")
    )
    mocker.patch.object(
        Auth, "verify_token",
        return_value={"sub": "1", "role": "Sales"}
    )

    payload = Auth.is_authenticated()

    assert payload["sub"] == "1"
    assert payload["role"] == "Sales"


def test_is_authenticated_expired_token_refresh_success(mocker):
    """Test du rafraîchissement d'un token expiré avec succès."""
    mocker.patch.object(Auth, "load_token", return_value=("expired_token", "valid_refresh_token"))
    mocker.patch.object(Auth, "verify_token", side_effect=["expired", {"sub": "1", "role": "Sales"}])
    mocker.patch.object(Auth, "create_access_token", return_value="new_access_token")
    mocker.patch.object(Auth, "save_token")

    payload = Auth.is_authenticated()

    assert payload["sub"] == "1"
    assert payload["role"] == "Sales"
