import pytest
from models.permission import role_required

def test_role_required_valid():
    """Test `@role_required` allow access with valid role."""

    @role_required("Management")
    def protected_function(user_payload):
        return "Access granted"

    user_payload = {"sub": "1", "role": "Management"}
    result = protected_function(user_payload)

    assert result == "Access granted"

def test_role_required_invalid():
    """Test `@role_required` restrain access with invalid role."""

    @role_required("Management")
    def protected_function(user_payload):
        return "This should not be reached"

    user_payload = {"sub": "1", "role": "Sales"}

    with pytest.raises(
        PermissionError,
        match="Access denied: Role 'Sales' not authorized for this action"
    ):
        protected_function(user_payload)
