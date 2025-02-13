from sqlalchemy.orm import Session
from repository.customer_repository import CustomerRepository
from models.customer import Customer


class CustomerService:
    """Handles business logic for customers."""

    @staticmethod
    def get_by_id(session: Session, customer_id: int):
        """Retrieves a customer by ID."""
        return CustomerRepository.get_customer_by_id(session, customer_id)

    @staticmethod
    def list_all(session: Session):
        """Get all clients as dictionnaries."""
        customers = CustomerRepository.get_all_customers(session)
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "company": customer.company_name,
                "email": customer.email,
                "phone": customer.phone,
                "sales_contact_id": customer.sales_contact_id
            }
            for customer in customers
        ]

    @staticmethod
    def check_if_customer_exists(
        session: Session,
        email: str,
        company_name: str,
        phone: str
    ) -> bool:
        """Check if customer already exist."""
        return any(
            [
                CustomerRepository.get_customer_by_email(session, email),
                CustomerRepository.get_customer_by_company_name(session,
                                                                company_name),
                CustomerRepository.get_customer_by_phone(session, phone),
            ]
        )

    def create(
        session: Session,
        name: str,
        company_name: str,
        email: str,
        phone: str,
        sales_contact_id: int
    ):
        """Creates a new customer."""

        if CustomerService.check_if_customer_exists(
            session,
            email,
            company_name, phone
        ):
            raise ValueError(
                "A customer with this email, "
                "company name, or phone number already exists."
            )

        customer = Customer(
            name=name,
            company_name=company_name,
            email=email,
            phone=phone,
            sales_contact_id=sales_contact_id
        )

        return CustomerRepository.save(session, customer)

    @staticmethod
    def update(session: Session, customer_id: int, data: dict):
        """Update an existing customer."""
        event = CustomerRepository.get_customer_by_id(session, customer_id)
        if not event:
            raise ValueError("Customer not found.")
        return CustomerRepository.update_customer(session, customer_id, data)

    @staticmethod
    def delete(session: Session, customer_id: int):
        """Delete a customer."""
        customer = CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise ValueError("Customer not found.")

        return CustomerRepository.delete_customer(session, customer_id)
