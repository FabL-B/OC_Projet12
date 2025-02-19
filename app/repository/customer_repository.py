from sqlalchemy.orm import Session
from app.models import Customer


class CustomerRepository:
    """Handles database operations related to the Customer entity."""
    @staticmethod
    def create_customer(session: Session, customer: Customer):
        """Create a new customer in data base."""
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    @staticmethod
    def update_customer(session: Session, customer_id: int, data: dict):
        """Update an existing customer in database."""
        customer = session.get(Customer, customer_id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
            session.commit()
        return customer

    @staticmethod
    def delete_customer(session: Session, customer_id: int):
        """Delete a customer frome database."""
        customer = session.get(Customer, customer_id)
        session.delete(customer)
        session.commit()
        return customer

    @staticmethod
    def get_customer_by_id(session: Session, customer_id: int):
        """Get customer from database with its ID."""
        return session.get(Customer, customer_id)

    @staticmethod
    def get_customer_by_email(session: Session, customer_email: str):
        """Get customer from database with its email."""
        return session.query(Customer).filter_by(email=customer_email).first()

    @staticmethod
    def get_customer_by_company_name(session: Session, company_name: str):
        """Get customer from database with its company name."""
        return session.query(Customer).filter_by(
            company_name=company_name).first()

    @staticmethod
    def get_customer_by_phone(session: Session, phone: str):
        """Get customer from database with its phone number."""
        return session.query(Customer).filter_by(phone=phone).first()

    @staticmethod
    def get_all_customers(session: Session):
        """Get all customers from database in a list."""
        return session.query(Customer).all()

    @staticmethod
    def get_customers_by_sales_id(session: Session, sales_contact_id: int):
        """Retrieves all customers managed by a specific sales."""
        return session.query(Customer).filter_by(
            sales_contact_id=sales_contact_id).all()
