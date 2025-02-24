import pytest
from app.permissions.permission import (
    UserPermission, CustomerPermission, ContractPermission, EventPermission,
    permission_required
)


# Simulate users
user_admin = {"id": 1, "role": "Admin"}
user_management = {"id": 2, "role": "Management"}
user_sales_ok = {"id": 3, "role": "Sales"}
user_sales_nok = {"id": 10, "role": "Sales"}
user_support_ok = {"id": 4, "role": "Support"}
user_support_nok = {"id": 20, "role": "Support"}
user_random = {"id": 5, "role": "random"}

# Simulate objects
class MockCustomer:
    def __init__(self, sales_contact_id):
        self.sales_contact_id = sales_contact_id

class MockContract:
    def __init__(self, customer):
        self.customer = customer

class MockEvent:
    def __init__(self, contract, support_contact_id):
        self.contract = contract
        self.support_contact_id = support_contact_id

# Mock data
customer_sales = MockCustomer(sales_contact_id=3)
contract_sales = MockContract(customer=customer_sales)
event_sales_signed = MockEvent(contract=contract_sales, support_contact_id=4)
event_sales_signed.contract.is_signed = True
event_sales_unsigned = MockEvent(contract=contract_sales, support_contact_id=4)
event_sales_unsigned.contract.is_signed = False


def test_user_permission():
    """Test des permissions générales pour UserPermission."""
    permission_admin = UserPermission(user_admin)
    permission_management = UserPermission(user_management)
    permission_sales = UserPermission(user_sales_ok)

    # ✅ Admin a accès à tout
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_permission("update") is True
    assert permission_admin.has_permission("delete") is True

    # ✅ Management peut tout sauf `list_all`
    assert permission_management.has_permission("create") is True
    assert permission_management.has_permission("update") is True
    assert permission_management.has_permission("delete") is True

    # ❌ Sales ne peut rien faire sur les utilisateurs
    assert permission_sales.has_permission("create") is False
    assert permission_sales.has_permission("update") is False
    assert permission_sales.has_permission("delete") is False


def test_customer_permission():
    """Test des permissions générales pour CustomerPermission."""
    permission_sales = CustomerPermission(user_sales_ok)
    permission_admin = CustomerPermission(user_admin)

    # ✅ Sales peut créer un client
    assert permission_sales.has_permission("create") is True

    # ✅ Admin a accès à tout
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_object_permission(customer_sales, "update") is True
    assert permission_admin.has_object_permission(customer_sales, "delete") is True

    # ❌ Sales ne peut modifier un client que s'il en est responsable
    permission_sales_nok = CustomerPermission(user_sales_nok)
    assert permission_sales_nok.has_object_permission(customer_sales, "update") is False


def test_contract_permission():
    """Test des permissions générales pour ContractPermission."""
    permission_management = ContractPermission(user_management)
    permission_sales = ContractPermission(user_sales_ok)
    permission_admin = ContractPermission(user_admin)

    # ✅ Management peut créer un contrat
    assert permission_management.has_permission("create") is True

    # ✅ Admin a accès à tout
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_object_permission(contract_sales, "update") is True
    assert permission_admin.has_object_permission(contract_sales, "delete") is True

    # ❌ Sales ne peut modifier un contrat que si son client lui appartient
    permission_sales_nok = ContractPermission(user_sales_nok)
    assert permission_sales_nok.has_object_permission(contract_sales, "update") is False


def test_event_permission():
    """Test des permissions générales pour EventPermission."""
    permission_sales = EventPermission(user_sales_ok)
    permission_support = EventPermission(user_support_ok)
    permission_admin = EventPermission(user_admin)

    # ✅ Sales peut créer un événement si le contrat est signé
    assert permission_sales.has_object_permission(event_sales_signed, "create") is True
    assert permission_sales.has_object_permission(event_sales_unsigned, "create") is False

    # ✅ Admin a accès à tout
    assert permission_admin.has_permission("create") is True
    assert permission_admin.has_object_permission(event_sales_signed, "update") is True

    # ❌ Support ne peut modifier un événement que s'il y est assigné
    permission_support_nok = EventPermission(user_support_nok)
    assert permission_support_nok.has_object_permission(event_sales_signed, "update") is False
