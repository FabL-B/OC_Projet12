from app.models.customer import Customer
from app.repository.customer_repository import CustomerRepository


def test_create_customer(mock_session):
    """Test the creation and saving of a customer in the database."""
    customer = Customer(
        name="Client A", company_name="Company A",
        email="clientA@example.com", phone="123456789", sales_contact_id=2
    )

    CustomerRepository.create_customer(mock_session, customer)

    assert mock_session.add.called
    assert mock_session.commit.called


def test_get_customer_by_id(mock_session):
    """Test retrieving a customer by ID."""
    customer = Customer(
        id=1, name="Client A", company_name="Company A",
        email="clientA@example.com", phone="123456789"
    )
    mock_session.get.return_value = customer

    result = CustomerRepository.get_customer_by_id(mock_session, 1)

    assert result == customer


def test_delete_customer(mock_session):
    """Test deleting a customer from the database."""
    customer = Customer(
        id=1, name="Client A", company_name="Company A",
        email="clientA@example.com", phone="123456789"
    )
    mock_session.get.return_value = customer

    result = CustomerRepository.delete_customer(mock_session, 1)

    assert mock_session.delete.called
    assert mock_session.commit.called
    assert result == customer
