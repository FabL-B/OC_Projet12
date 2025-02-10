from sqlalchemy.orm import Session
from models.auth import auth_required
from services.customer_service import CustomerService


class CustomerController:
    """Controler to handle customers."""

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
