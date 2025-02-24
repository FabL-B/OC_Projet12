import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.repository.customer_repository import CustomerRepository
from app.models.customer import Customer
from app.services.customer_service import CustomerService  # Import your service class

class TestCustomerService(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock(spec=Session)
        self.customer_data = {
            "name": "Test Customer",
            "company_name": "Test Company",
            "email": "test@example.com",
            "phone": "123-456-7890",
            "sales_contact_id": 1
        }

    def test_get_by_id(self):
        mock_customer = MagicMock(spec=Customer)
        CustomerRepository.get_customer_by_id = MagicMock(return_value=mock_customer)
        customer = CustomerService.get_by_id(self.session_mock, 1)
        self.assertEqual(customer, mock_customer)
        CustomerRepository.get_customer_by_id.assert_called_once_with(self.session_mock, 1)

    def test_get_by_id_not_found(self):
        CustomerRepository.get_customer_by_id = MagicMock(return_value=None)
        with self.assertRaises(ValueError) as context:
            CustomerService.get_by_id(self.session_mock, 1)
        self.assertEqual(str(context.exception), "Customer not found.")

    def test_list_all(self):
        mock_customers = [
            Customer(id=1, name="Cust 1", company_name="Comp 1", email="c1@example.com", phone="111", sales_contact_id=1),
            Customer(id=2, name="Cust 2", company_name="Comp 2", email="c2@example.com", phone="222", sales_contact_id=2),
        ]
        CustomerRepository.get_all_customers = MagicMock(return_value=mock_customers)
        customers = CustomerService.list_all(self.session_mock)
        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[0]["id"], 1)
        CustomerRepository.get_all_customers.assert_called_once_with(self.session_mock)

    def test_list_by_sales_id(self):
        mock_customers = [
            Customer(id=1, name="Cust 1", company_name="Comp 1", email="c1@example.com", phone="111", sales_contact_id=1),
        ]
        CustomerRepository.get_customers_by_sales_id = MagicMock(return_value=mock_customers)
        customers = CustomerService.list_by_sales_id(self.session_mock, 1)
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["id"], 1)
        CustomerRepository.get_customers_by_sales_id.assert_called_once_with(self.session_mock, 1)

    @patch("app.services.customer_service.CustomerService.check_if_customer_exists")  # Patch the method itself
    @patch("app.services.customer_service.CustomerRepository.create_customer")
    def test_create(self, mock_create_customer, mock_check_exists):
        mock_check_exists.return_value = False  # Customer doesn't exist
        mock_customer = MagicMock(spec=Customer)
        mock_create_customer.return_value = mock_customer

        customer = CustomerService.create(self.session_mock, self.customer_data["name"], self.customer_data["company_name"],
                                          self.customer_data["email"], self.customer_data["phone"], self.customer_data["sales_contact_id"])

        self.assertEqual(customer, mock_customer)
        mock_check_exists.assert_called_once_with(self.session_mock, self.customer_data["email"], self.customer_data["company_name"], self.customer_data["phone"])
        mock_create_customer.assert_called_once()


    @patch("app.services.customer_service.CustomerService.check_if_customer_exists")
    def test_create_existing_customer(self, mock_check_exists):
        mock_check_exists.return_value = True  # Customer exists
        with self.assertRaises(ValueError) as context:
            CustomerService.create(self.session_mock, self.customer_data["name"], self.customer_data["company_name"],
                                  self.customer_data["email"], self.customer_data["phone"], self.customer_data["sales_contact_id"])
        self.assertEqual(str(context.exception), "A customer with this email, company name, or phone number already exists.")

    @patch("app.services.customer_service.CustomerRepository.get_customer_by_id")
    @patch("app.services.customer_service.CustomerRepository.update_customer")
    def test_update(self, mock_update_customer, mock_get_customer_by_id):
        mock_customer = MagicMock(spec=Customer)
        mock_get_customer_by_id.return_value = mock_customer
        updated_data = {"name": "Updated Name"}
        updated_customer = CustomerService.update(self.session_mock, 1, updated_data)
        self.assertEqual(updated_customer, mock_update_customer.return_value) # Or mock_customer if the method returns the updated object
        mock_get_customer_by_id.assert_called_once_with(self.session_mock, 1)
        mock_update_customer.assert_called_once_with(self.session_mock, 1, updated_data)

    @patch("app.services.customer_service.CustomerRepository.get_customer_by_id")
    def test_update_customer_not_found(self, mock_get_customer_by_id):
        mock_get_customer_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            CustomerService.update(self.session_mock, 1, {"name": "Updated Name"})
        self.assertEqual(str(context.exception), "Customer not found.")

    @patch("app.services.customer_service.CustomerRepository.get_customer_by_id")
    @patch("app.services.customer_service.CustomerRepository.delete_customer")
    def test_delete(self, mock_delete_customer, mock_get_customer_by_id):
        mock_customer = MagicMock(spec=Customer)
        mock_get_customer_by_id.return_value = mock_customer
        deleted = CustomerService.delete(self.session_mock, 1)
        self.assertEqual(deleted, mock_delete_customer.return_value) # Or True if the method returns a boolean
        mock_get_customer_by_id.assert_called_once_with(self.session_mock, 1)
        mock_delete_customer.assert_called_once_with(self.session_mock, 1)

    @patch("app.services.customer_service.CustomerRepository.get_customer_by_id")
    def test_delete_customer_not_found(self, mock_get_customer_by_id):
        mock_get_customer_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            CustomerService.delete(self.session_mock, 1)
        self.assertEqual(str(context.exception), "Customer not found.")

    @patch("app.services.customer_service.CustomerRepository.get_customer_by_email")
    @patch("app.services.customer_service.CustomerRepository.get_customer_by_company_name")
    @patch("app.services.customer_service.CustomerRepository.get_customer_by_phone")
    def test_check_if_customer_exists(self, mock_get_by_phone, mock_get_by_company_name, mock_get_by_email):
        # Test case 1: No customer exists
        mock_get_by_email.return_value = None
        mock_get_by_company_name.return_value = None
        mock_get_by_phone.return_value = None
        self.assertFalse(CustomerService.check_if_customer_exists(self.session_mock, "test@example.com", "Test Company", "123-456-7890"))

        # Test case 2: Customer exists with matching email
        mock_get_by_email.return_value = MagicMock(spec=Customer)  # Simulate a Customer object
        mock_get_by_company_name.return_value = None
        mock_get_by_phone.return_value = None
        self.assertTrue(CustomerService.check_if_customer_exists(self.session_mock, "test@example.com", "Different Company", "Different Phone"))

        # Test case 3: Customer exists with matching company name
        mock_get_by_email.return_value = None
        mock_get_by_company_name.return_value = MagicMock(spec=Customer)
        mock_get_by_phone.return_value = None
        self.assertTrue(CustomerService.check_if_customer_exists(self.session_mock, "Different Email", "Test Company", "Different Phone"))

        # Test case 4: Customer exists with matching phone
        mock_get_by_email.return_value = None
        mock_get_by_company_name.return_value = None
        mock_get_by_phone.return_value = MagicMock(spec=Customer)
        self.assertTrue(CustomerService.check_if_customer_exists(self.session_mock, "Different Email", "Different Company", "123-456-7890"))

        # Test case 5: Customer exists with matching email and company name (or any combination)
        mock_get_by_email.return_value = MagicMock(spec=Customer)
        mock_get_by_company_name.return_value = MagicMock(spec=Customer)
        mock_get_by_phone.return_value = None
        self.assertTrue(CustomerService.check_if_customer_exists(self.session_mock, "test@example.com", "Test Company", "Different Phone"))

        # Ensure all repository methods were called (optional, but good practice)
        mock_get_by_email.assert_any_call(self.session_mock, "test@example.com")
        mock_get_by_company_name.assert_any_call(self.session_mock, "Test Company")
        mock_get_by_phone.assert_any_call(self.session_mock, "123-456-7890")



if __name__ == '__main__':
    unittest.main()