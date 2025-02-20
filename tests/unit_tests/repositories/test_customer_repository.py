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

    created_customer = CustomerRepository.create_customer(
        mock_session, customer
    )

    mock_session.add.assert_called_once_with(customer)
    mock_session.commit.assert_called_once()
    assert created_customer == customer
