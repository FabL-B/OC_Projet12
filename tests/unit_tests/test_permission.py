import pytest
from models.permission import (
    UserPermission, CustomerPermission, ContractPermission, EventPermission,
    permission_required
)

# Simulate users
user_management = {"id": 1, "role": "Management"}
user_sales_ok = {"id": 2, "role": "Sales"}
user_sales_nok = {"id": 10, "role": "Sales"}
user_support_ok = {"id": 3, "role": "Support"}
user_support_nok = {"id": 20, "role": "Support"}
user_random = {"id": 4, "role": "random"}


# Simulate objects
class MockCustomer:
    def __init__(self, sales_user_id):
        self.sales_user_id = sales_user_id


class MockContract:
    def __init__(self, customer):
        self.customer = customer


class MockEvent:
    def __init__(self, contract, support_user_id):
        self.contract = contract
        self.support_user_id = support_user_id


# customer related to user_sales_ok
customer_sales = MockCustomer(sales_user_id=2)
contract_sales = MockContract(customer=customer_sales)
event_sales_signed = MockEvent(contract=contract_sales, support_user_id=3)
event_sales_signed.contract.is_signed = True


def test_user_permission():
    permission = UserPermission()

    assert permission.has_permission(user_management, "create") is True
    assert permission.has_permission(user_sales_ok, "create") is False

    assert permission.has_permission(user_management, "delete") is True
    assert permission.has_permission(user_sales_ok, "delete") is False

    assert permission.has_permission(user_management, "list_all") is True
    assert permission.has_permission(user_sales_ok, "list_all") is True


def test_customer_permission():
    permission = CustomerPermission()

    assert permission.has_permission(
        user_sales_ok, "list_all") is True

    assert permission.has_permission(
        user_sales_ok, "create") is True
    assert permission.has_permission(
        user_management, "create") is False

    assert permission.has_object_permission(
        user_sales_ok, customer_sales, "update") is True
    assert permission.has_object_permission(
        user_sales_nok, customer_sales, "update") is False
    assert permission.has_object_permission(
        user_management, customer_sales, "update") is False


def test_contract_permission():
    permission = ContractPermission()

    assert permission.has_permission(
        user_sales_ok, "lsit_all") is True
    assert permission.has_permission(
        user_management, "lsit_all") is True

    assert permission.has_permission(
        user_management, "create") is True
    assert permission.has_permission(
        user_sales_ok, "create") is False

    assert permission.has_object_permission(
        user_sales_ok, contract_sales, "update") is True
    # Sales not related to contract's customer
    assert permission.has_object_permission(
        user_sales_nok, contract_sales, "update") is False
    assert permission.has_object_permission(
        user_random, contract_sales, "update") is False


def test_event_permission():
    permission = EventPermission()

    assert permission.has_permission(user_sales_ok, "list_all") is True
    assert permission.has_permission(user_management, "list_all") is True

    assert permission.has_permission(user_sales_ok, "create") is True
    assert permission.has_permission(user_management, "create") is False

    assert permission.has_object_permission(
        user_sales_ok, event_sales_signed, "create") is True
    # Sales not related event's customer
    assert permission.has_object_permission(
        user_sales_nok, event_sales_signed, "create") is False
    assert permission.has_object_permission(
        user_support_ok, event_sales_signed, "create") is False

    assert permission.has_object_permission(
        user_support_ok, event_sales_signed, "update") is True
    assert permission.has_object_permission(
        user_support_nok, event_sales_signed, "update") is False
    assert permission.has_object_permission(
        user_sales_ok, event_sales_signed, "update") is False


def test_create_user_permission():
    """Test if a Management user has the permission to create a user."""
    permission = UserPermission()
    assert permission.has_permission({"role": "Management"}, "create") is True
    assert permission.has_permission({"role": "management"}, "create") is False

    assert permission.has_permission({"role": "SALES"}, "create") is False


def test_user_permission_wrapper(mocker):
    mocker.patch.object(
        UserPermission,
        "has_permission",
        side_effect=lambda user,
        action: user["role"] == "Management"
    )

    class FakeUserController:
        permission_class = UserPermission

        @permission_required("create")
        def create_user(self, user_payload):
            return "User created"

    controller = FakeUserController()

    assert controller.create_user(user_management) == "User created"

    with pytest.raises(PermissionError, match="Access denied"):
        controller.create_user(user_sales_ok)


def test_customer_permission_wrapper(mocker):
    mocker.patch.object(
        CustomerPermission,
        "has_permission",
        side_effect=lambda user,
        action: user["role"] == "Sales"
    )

    class FakeCustomerController:
        permission_class = CustomerPermission

        @permission_required("create")
        def create_customer(self, user_payload):
            return "Customer created"

    controller = FakeCustomerController()

    assert controller.create_customer(user_sales_ok) == "Customer created"

    with pytest.raises(PermissionError, match="Access denied"):
        controller.create_customer(user_management)


def test_contract_permission_wrapper(mocker):
    mocker.patch.object(
        ContractPermission,
        "has_permission",
        side_effect=lambda user,
        action: user["role"] == "Management"
    )

    class FakeContractController:
        permission_class = ContractPermission

        @permission_required("create")
        def create_contract(self, user_payload):
            return "Contract created"

    controller = FakeContractController()

    assert controller.create_contract(user_management) == "Contract created"

    with pytest.raises(PermissionError, match="Access denied"):
        controller.create_contract(user_sales_ok)


def test_event_permission_wrapper(mocker):
    mocker.patch.object(
        EventPermission,
        "has_permission",
        side_effect=lambda user,
        action: user["role"] == "Sales"
    )

    class FakeEventController:
        permission_class = EventPermission

        @permission_required("create")
        def create_event(self, user_payload):
            return "Event created"

    controller = FakeEventController()

    assert controller.create_event(user_sales_ok) == "Event created"

    with pytest.raises(PermissionError, match="Access denied"):
        controller.create_event(user_management)
