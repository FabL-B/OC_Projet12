import re
from app.repository.customer_repository import CustomerRepository
from app.models.customer import Customer
from app.utils.transaction import transactional_session
from app.repository.user_repository import UserRepository


class CustomerService:
    """Handles business logic for customers."""

    @staticmethod
    def validate_email(email):
        """Validates that the email format is correct."""
        email_regex = (
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )
        if not re.match(email_regex, email):
            raise ValueError(
                "Invalid email format. Please use a valid email address."
            )
        return email

    @staticmethod
    def validate_phone(phone):
        """Validates that the phone format is correct. (10-15 numbers)."""
        phone_regex = r"^\+?\d{10,15}$"

        if not re.match(phone_regex, phone):
            raise ValueError(
                "Invalid phone format."
                "Please use a valid number (e.g., +33123456789)."
            )

        return phone

    @staticmethod
    def get_by_id(session, customer_id):
        """Retrieves a customer by ID."""
        customer = CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise ValueError("Customer not found.")
        return customer

    @staticmethod
    def list_all(session):
        """Get all customers as dictionaries."""
        customers = CustomerRepository.get_all_customers(session)
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "company_name": customer.company_name,
                "email": customer.email,
                "phone": customer.phone,
                "sales_contact_id": customer.sales_contact_id
            }
            for customer in customers
        ]

    @staticmethod
    def list_by_sales_id(session, sales_contact_id):
        """Get all customers managed by a specific sales."""
        customers = CustomerRepository.get_customers_by_sales_id(
            session, sales_contact_id)
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "company_name": customer.company_name,
                "email": customer.email,
                "phone": customer.phone
            }
            for customer in customers
        ]

    @staticmethod
    def check_if_customer_exists(session, email, company_name, phone):
        """Check if customer exists."""
        return any(
            [
                CustomerRepository.get_customer_by_email(session, email),
                CustomerRepository.get_customer_by_company_name(session,
                                                                company_name),
                CustomerRepository.get_customer_by_phone(session, phone),
            ]
        )

    @staticmethod
    def create(session, name, company_name, email, phone, sales_contact_id):
        """Creates a new customer."""
        with transactional_session(session) as s:
            CustomerService.validate_email(email)
            CustomerService.validate_phone(phone)
            if CustomerService.check_if_customer_exists(
                    s, email, company_name, phone
            ):
                raise ValueError(
                    "A customer with this email, company name, "
                    "or phone number already exists."
                )
            customer = Customer(
                name=name,
                company_name=company_name,
                email=email,
                phone=phone,
                sales_contact_id=sales_contact_id
            )
            return CustomerRepository.create_customer(session, customer)

    @staticmethod
    def update(session, customer_id, data):
        """Update an existing customer."""
        with transactional_session(session) as s:
            customer = CustomerRepository.get_customer_by_id(s, customer_id)
            if not customer:
                raise ValueError("Customer not found.")
            if "email" in data:
                CustomerService.validate_email(data["email"])
            if "phone" in data:
                CustomerService.validate_phone(data["phone"])
            if "sales_contact_id" in data:
                sales_contact = UserRepository.get_user_by_id(
                    s,
                    data["sales_contact_id"]
                )
                if not sales_contact:
                    raise ValueError("Sales contact ID not found.")
            return CustomerRepository.update_customer(s, customer_id, data)

    @staticmethod
    def delete(session, customer_id):
        """Delete a customer."""
        with transactional_session(session) as s:
            customer = CustomerRepository.get_customer_by_id(s, customer_id)
            if not customer:
                raise ValueError("Customer not found.")
            return CustomerRepository.delete_customer(s, customer_id)

    @staticmethod
    def list_customers_without_sales_contact(session):
        """Returns all customers without an assigned sales contact."""
        customers = CustomerRepository.get_customers_without_sales_contact(
            session
        )
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "company_name": customer.company_name,
                "email": customer.email,
                "phone": customer.phone
            }
            for customer in customers
        ]
