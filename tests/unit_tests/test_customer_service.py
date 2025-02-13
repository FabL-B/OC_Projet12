from models.customer import Customer
from services.customer_service import CustomerService
from repository.customer_repository import CustomerRepository


def test_delete_customer_success(mock_session, mocker):
    """Test successful customer deletion."""
    fake_customer = Customer(
        id=1, name="Client A", email="clientA@example.com", phone="123456789"
    )

    mocker.patch.object(
        CustomerRepository,
        "get_customer_by_id",
        return_value=fake_customer,
    )
    mocker.patch.object(
        CustomerRepository,
        "delete_customer",
        return_value=fake_customer,
    )

    deleted_customer = CustomerService.delete(mock_session, 1)

    assert deleted_customer == fake_customer
