from unittest.mock import MagicMock
from app.models import Customer
from app.repository.customer_repository import CustomerRepository


def test_create_customer():
    mock_session = MagicMock()
    customer = Customer(
        id=1,
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890", sales_contact_id=1
        )

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    created_customer = CustomerRepository.create_customer(
        mock_session, customer
    )

    mock_session.add.assert_called_once_with(customer)
    mock_session.commit.assert_called_once()
    assert created_customer == customer


def test_get_customer_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = Customer(
        id=1,
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890", sales_contact_id=1
        )

    retrieved_customer = CustomerRepository.get_customer_by_id(mock_session, 1)

    mock_session.get.assert_called_once_with(Customer, 1)
    assert retrieved_customer.email == "client@example.com"


def test_update_customer():
    mock_session = MagicMock()
    customer = Customer(
        id=1,
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890", sales_contact_id=1
        )
    mock_session.get.return_value = customer

    updated_data = {
        "name": "Updated Client C",
        "email": "updatedC@example.com"
    }
    updated_customer = CustomerRepository.update_customer(
        mock_session,
        1,
        updated_data
    )

    mock_session.get.assert_called_once_with(Customer, 1)
    assert updated_customer.name == "Updated Client C"
    assert updated_customer.email == "updatedC@example.com"


def test_delete_customer():
    mock_session = MagicMock()
    customer = Customer(
        id=1,
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890", sales_contact_id=1
        )
    mock_session.get.return_value = customer

    deleted_customer = CustomerRepository.delete_customer(mock_session, 1)

    mock_session.get.assert_called_once_with(Customer, 1)
    mock_session.delete.assert_called_once_with(customer)
    assert deleted_customer == customer
