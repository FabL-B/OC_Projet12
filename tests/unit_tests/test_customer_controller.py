import pytest
from models.customer import Customer
from controllers.customer_controller import CustomerController
from services.customer_service import CustomerService
from models.auth import Auth
from models.permission import CustomerPermission


@pytest.fixture
def customer_controller():
    """Fixture to instantiate CustomerController."""
    return CustomerController()


def test_list_all_customers(mocker, customer_controller, mock_session):
    """Test retrieving all customers."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        CustomerService,
        "list_all",
        return_value=[
            Customer(id=1, name="Client A"),
            Customer(id=2, name="Client B"),
        ],
    )

    customers = customer_controller.list_all(mock_session)

    assert len(customers) == 2
    assert customers[0].name == "Client A"
    assert customers[1].name == "Client B"
    CustomerService.list_all.assert_called_once_with(mock_session)


def test_get_customer(mocker, customer_controller, mock_session):
    """Test retrieving a specific customer."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        CustomerService,
        "get_by_id",
        return_value=Customer(id=1, name="Client A"),
    )

    customer = customer_controller.get(mock_session, entity_id=1)

    assert customer.name == "Client A"
    CustomerService.get_by_id.assert_called_once_with(mock_session, 1)


def test_create_customer(mocker, customer_controller, mock_session):
    """Test creating a customer."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        CustomerService,
        "create",
        return_value=Customer(id=1, name="Client A"),
    )
    mocker.patch.object(
        CustomerPermission,
        "has_permission",
        return_value=True,
    )

    customer_controller.create(
        mock_session,
        name="Client A",
        email="clientA@example.com",
        phone="123456789",
    )

    CustomerService.create.assert_called_once_with(
        mock_session,
        name="Client A",
        email="clientA@example.com",
        phone="123456789",
    )


def test_update_customer(mocker, customer_controller, mock_session):
    """Test updating a customer."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(CustomerService, "update", return_value=True)

    success = customer_controller.update(
        mock_session, entity_id=1, data={"name": "Client A Updated"}
    )

    assert success is True
    CustomerService.update.assert_called_once_with(
        mock_session, 1, {"name": "Client A Updated"}
    )


def test_delete_customer(mocker, customer_controller, mock_session):
    """Test deleting a customer."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(CustomerService, "delete", return_value=True)

    success = customer_controller.delete(mock_session, entity_id=1)

    assert success is True
    CustomerService.delete.assert_called_once_with(mock_session, 1)
