from sqlalchemy.orm import Session
from models.auth import auth_required
from services.customer_service import CustomerService


class CustomerController:
    """Controler to handle customers."""
    @staticmethod
    @auth_required
    def create_customer(
        user_payload,
        session: Session,
        name: str,
        company_name: str,
        email: str,
        phone: str,
        sales_contact_id: int
    ):
        """Create a new customer."""
        customer = CustomerService.create_customer(
            session,
            name,
            company_name,
            email,
            phone,
            sales_contact_id
        )
        print(f"Customer '{customer.name}' created successfully.")
        return customer

    @staticmethod
    @auth_required
    def update_customer(
        user_payload,
        session: Session,
        customer_id: int,
        data: dict
    ):
        """Update an existing customer."""
        customer = CustomerService.update_customer(
            session,
            customer_id, data
        )
        print(f"Customer '{customer.name}' updated successfully.")
        return customer

    @staticmethod
    @auth_required
    def delete_customer(user_payload, session: Session, customer_id: int):
        """Delete a customer"""
        customer = CustomerService.delete_customer(session, customer_id)
        print(f"Customer '{customer.name}' deleted successfully.")
        return customer

    @staticmethod
    @auth_required
    def list_customers(user_payload, session: Session):
        """List all clients."""
        customers = CustomerService.list_customers(session)
        return customers

    @staticmethod
    @auth_required
    def get_customer(user_payload, session: Session, customer_id: int):
        """Get customer with its ID."""
        try:
            return CustomerService.get_customer_by_id(session, customer_id)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
