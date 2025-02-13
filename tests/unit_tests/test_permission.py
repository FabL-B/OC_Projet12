from models.permission import (
    UserPermission, CustomerPermission, ContractPermission, EventPermission
)

# Simulate users
user_management = {"id": 1, "role": "management"}
user_sales_ok = {"id": 2, "role": "sales"}
user_sales_nok = {"id": 10, "role": "sales"}
user_support_ok = {"id": 3, "role": "support"}
user_support_nok = {"id": 20, "role": "support"}
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

    assert permission.has_permission(user_management, "create_user") is True
    assert permission.has_permission(user_sales_ok, "create_user") is False

    assert permission.has_permission(user_management, "delete_user") is True
    assert permission.has_permission(user_sales_ok, "delete_user") is False

    assert permission.has_permission(user_management, "get_all_users") is True
    assert permission.has_permission(user_sales_ok, "get_all_users") is True


def test_customer_permission():
    permission = CustomerPermission()

    assert permission.has_permission(
        user_sales_ok, "get_all_customers") is True

    assert permission.has_permission(
        user_sales_ok, "create_customer") is True
    assert permission.has_permission(
        user_management, "create_customer") is False

    assert permission.has_object_permission(
        user_sales_ok, customer_sales, "edit_customer") is True
    assert permission.has_object_permission(
        user_sales_nok, customer_sales, "edit_customer") is False
    assert permission.has_object_permission(
        user_management, customer_sales, "edit_customer") is False


def test_contract_permission():
    permission = ContractPermission()

    assert permission.has_permission(
        user_sales_ok, "get_all_contracts") is True
    assert permission.has_permission(
        user_management, "get_all_contracts") is True

    assert permission.has_permission(
        user_management, "create_contract") is True
    assert permission.has_permission(
        user_sales_ok, "create_contract") is False

    assert permission.has_object_permission(
        user_sales_ok, contract_sales, "update_contract") is True
    # Sales not related to contract's customer
    assert permission.has_object_permission(
        user_sales_nok, contract_sales, "update_contract") is False
    assert permission.has_object_permission(
        user_random, contract_sales, "update_contract") is False


def test_event_permission():
    permission = EventPermission()

    assert permission.has_permission(user_sales_ok, "get_all_events") is True
    assert permission.has_permission(user_management, "get_all_events") is True

    assert permission.has_permission(user_sales_ok, "create_event") is True
    assert permission.has_permission(user_management, "create_event") is False

    assert permission.has_object_permission(
        user_sales_ok, event_sales_signed, "create_event") is True
    # Sales not related event's customer
    assert permission.has_object_permission(
        user_sales_nok, event_sales_signed, "create_event") is False
    assert permission.has_object_permission(
        user_support_ok, event_sales_signed, "create_event") is False

    assert permission.has_object_permission(
        user_support_ok, event_sales_signed, "update_event") is True
    assert permission.has_object_permission(
        user_support_nok, event_sales_signed, "update_event") is False
    assert permission.has_object_permission(
        user_sales_ok, event_sales_signed, "update_event") is False
