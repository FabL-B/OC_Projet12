from models.customer import Customer
from services.customer_service import CustomerService
from repository.customer_repository import CustomerRepository


def test_delete_customer_success(mock_session, mocker):
    """Test successful delete of a customer."""
    fake_customer = Customer(id=1, name="Alice", company_name="ACME Corp")

    mocker.patch.object(
        CustomerRepository, "get_customer_by_id", return_value=fake_customer)
    mocker.patch.object(
        CustomerRepository, "delete_customer", return_value=fake_customer)

    deleted_customer = CustomerService.delete_customer(mock_session, 1)

    assert deleted_customer == fake_customer
