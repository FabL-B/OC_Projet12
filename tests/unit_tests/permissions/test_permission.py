import pytest
from unittest.mock import MagicMock
from app.permissions.permission import (
    UserPermission, CustomerPermission, ContractPermission, EventPermission,
    permission_required
)


# Simulated users
user_admin = {"id": 1, "role": "Admin"}
user_management = {"id": 2, "role": "Management"}
user_sales_ok = {"id": 3, "role": "Sales"}
user_sales_nok = {"id": 10, "role": "Sales"}
user_support_ok = {"id": 4, "role": "Support"}
user_support_nok = {"id": 20, "role": "Support"}
user_random = {"id": 5, "role": "random"}


# Simulated objects
class MockCustomer:
    """Mock class representing a Customer."""

    def __init__(self, sales_contact_id):
        self.sales_contact_id = sales_contact_id


class MockContract:
    """Mock class representing a Contract."""

    def __init__(self, customer):
        self.customer = customer


class MockEvent:
    """Mock class representing an Event."""

    def __init__(self, contract, support_contact_id):
        self.contract = contract
        self.support_contact_id = support_contact_id


class MockController:
    """Mock a controller using User permission."""
    permission_class = UserPermission

    @permission_required("create")
    def create(self, user_payload):
        return "Created!"

    @permission_required("delete", requires_object=True)
    def delete(self, user_payload, obj):
        return f"Deleted {obj.id}!"


# Mock data
customer_sales = MockCustomer(sales_contact_id=user_sales_ok["id"])

contract_sales_signed = MockContract(customer=customer_sales)
contract_sales_signed.is_signed = True  # Signed contract

contract_sales_unsigned = MockContract(customer=customer_sales)
contract_sales_unsigned.is_signed = False

event_sales_signed = MockEvent(
    contract=contract_sales_signed, support_contact_id=4
)
event_sales_unsigned = MockEvent(
    contract=contract_sales_unsigned, support_contact_id=4
)


def test_user_permission():
    """Tests general permissions for UserPermission."""
    permission_admin = UserPermission(user_admin)
    permission_management = UserPermission(user_management)
    permission_sales = UserPermission(user_sales_ok)

    # Admin has full access
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_permission("update") is True
    assert permission_admin.has_permission("delete") is True

    # Management can do everything except `list_all`
    assert permission_management.has_permission("create") is True
    assert permission_management.has_permission("update") is True
    assert permission_management.has_permission("delete") is True

    # Sales has no permissions for users
    assert permission_sales.has_permission("create") is False
    assert permission_sales.has_permission("update") is False
    assert permission_sales.has_permission("delete") is False


def test_customer_permission():
    """Tests general permissions for CustomerPermission."""
    permission_sales = CustomerPermission(user_sales_ok)
    permission_admin = CustomerPermission(user_admin)

    # Sales can create a customer
    assert permission_sales.has_permission("create") is True

    # Admin has full access
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_object_permission(
        customer_sales, "update"
    ) is True
    assert permission_admin.has_object_permission(
        customer_sales, "delete"
    ) is True

    # Sales can only modify a customer if they are responsible
    permission_sales_nok = CustomerPermission(user_sales_nok)
    assert permission_sales_nok.has_object_permission(
        customer_sales, "update"
    ) is False


def test_contract_permission():
    """Tests general permissions for ContractPermission."""
    permission_management = ContractPermission(user_management)
    permission_sales = ContractPermission(user_sales_ok)
    permission_sales_nok = ContractPermission(user_sales_nok)
    permission_admin = ContractPermission(user_admin)

    # Management can create a contract
    assert permission_management.has_permission("create") is True

    # Admin has full access
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_object_permission(
        contract_sales_signed, "update"
    ) is True
    assert permission_admin.has_object_permission(
        contract_sales_signed, "delete"
    ) is True

    # Sales can only modify a contract if their client belongs to them
    assert permission_sales.has_object_permission(
        contract_sales_signed, "update"
    ) is True
    assert permission_sales_nok.has_object_permission(
        contract_sales_signed, "update"
    ) is False


def test_event_permission():
    """Tests general permissions for EventPermission."""
    permission_sales = EventPermission(user_sales_ok)
    permission_support = EventPermission(user_support_ok)
    permission_admin = EventPermission(user_admin)
    permission_support_nok = EventPermission(user_support_nok)

    # Sales can create an event if the contract is signed
    assert permission_sales.has_object_permission(
        event_sales_signed, "create"
    ) is True
    assert permission_sales.has_object_permission(
        event_sales_unsigned, "create"
    ) is False

    # Admin has full access
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_object_permission(
        event_sales_signed, "update"
    ) is True

    # Support can only modify an event if they are assigned to it
    assert permission_support.has_object_permission(
        event_sales_signed, "update"
    ) is True
    assert permission_support_nok.has_object_permission(
        event_sales_signed, "update"
    ) is False


def test_wrapper_valid():
    """An Admin should have access to all actions."""
    mock_controller = MockController()
    user_admin = {"id": 1, "role": "Admin"}

    assert mock_controller.create(user_admin) == "Created!"
    assert mock_controller.delete(
        user_admin, obj=MagicMock(id=10)
    ) == "Deleted 10!"


def test_wrapper_denied():
    """
    A user without permissions should receive a PermissionError.
    """
    mock_controller = MockController()
    user_sales = {"id": 2, "role": "Sales"}  # Sales cannot create

    with pytest.raises(
        PermissionError, match="Access denied: No permission for create"
    ):
        mock_controller.create(user_sales)
