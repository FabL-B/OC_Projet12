from unittest.mock import MagicMock, patch
import pytest
from app.services.customer_service import CustomerService
from app.models.customer import Customer


def test_get_customer_by_id():
    """Test retrieving a customer by ID."""
    mock_session = MagicMock()
    mock_customer = Customer(
        id=1,
        name="Client A",
        email="client@example.com"
    )

    with patch(
        "app.repository.customer_repository.CustomerRepository.get_customer_by_id",  # noqa: E501
        return_value=mock_customer
    ):
        customer = CustomerService.get_by_id(mock_session, 1)

    assert customer.id == 1
    assert customer.name == "Client A"


def test_create_customer():
    """Test creating a new customer."""
    mock_session = MagicMock()
    mock_customer = Customer(
        id=2,
        name="Client B",
        email="clientB@example.com"
    )

    with patch(
        "app.services.customer_service.CustomerService.check_if_customer_exists",  # noqa: E501
        return_value=False
    ):
        with patch(
            "app.repository.customer_repository.CustomerRepository.create_customer",  # noqa: E501
            return_value=mock_customer
        ):
            created_customer = CustomerService.create(
                mock_session,
                "Client B",
                "Company B",
                "clientB@example.com",
                "+33123456789",
                1
            )

    assert created_customer.email == "clientB@example.com"


def test_create_customer_invalid():
    """Test validation errors for customer creation."""
    mock_session = MagicMock()

    with pytest.raises(ValueError, match="Invalid email format"):
        CustomerService.create(
            mock_session,
            "Client B",
            "Company B",
            "invalid-email",
            "+33123456789",
            1
        )

    with pytest.raises(ValueError, match="Invalid phone format"):
        CustomerService.create(
            mock_session,
            "Client B",
            "Company B",
            "clientB@example.com",
            "123",
            1
        )


def test_update_customer():
    """Test updating a customer's details."""
    mock_session = MagicMock()
    mock_customer = Customer(
        id=3,
        name="Client C",
        email="clientC@example.com"
    )
    updated_customer = Customer(
        id=3,
        name="Client C",
        email="updatedC@example.com"
    )

    with patch(
        "app.repository.customer_repository.CustomerRepository.get_customer_by_id",  # noqa: E501
        return_value=mock_customer
    ):
        with patch(
            "app.repository.customer_repository.CustomerRepository.update_customer",  # noqa: E501
            return_value=updated_customer
        ):
            result = CustomerService.update(
                mock_session,
                3,
                {"email": "updatedC@example.com"}
            )

    assert result.email == "updatedC@example.com"


def test_delete_customer():
    """Test deleting a customer."""
    mock_session = MagicMock()

    with patch(
        "app.repository.customer_repository.CustomerRepository.delete_customer",  # noqa: E501
        return_value=True
    ):
        result = CustomerService.delete(mock_session, 4)

    assert result is True
