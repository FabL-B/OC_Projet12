from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Customer


class CustomerRepository:
    """Handles database operations related to the Customer entity."""
    @staticmethod
    def save(session: Session, customer: Customer):
        """Save customer in data base."""
        try:
            session.add(customer)
            session.commit()
            session.refresh(customer)
            return customer
        except IntegrityError:
            session.rollback()
            raise ValueError("Customer already exists.")

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
