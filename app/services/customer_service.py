from app.repository.customer_repository import CustomerRepository
from app.models.customer import Customer
from app.utils.transaction import transactional_session


class CustomerService:
    """Handles business logic for customers."""

    @staticmethod
    def get_by_id(session, customer_id):
        """Retrieves a customer by ID."""
        customer = CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise ValueError("Customer not found.")
        return customer

    @staticmethod
    def list_all(session):
        """Get all clients as dictionnaries."""
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
        """Check if customer already exist."""
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
        if CustomerService.check_if_customer_exists(
                session, email, company_name, phone
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
            return CustomerRepository.update_customer(s, customer_id, data)

    @staticmethod
    def delete(session, customer_id):
        """Delete a customer."""
        with transactional_session(session) as s:
            customer = CustomerRepository.get_customer_by_id(s, customer_id)
            if not customer:
                raise ValueError("Customer not found.")
            return CustomerRepository.delete_customer(s, customer_id)
