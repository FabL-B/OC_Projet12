from app.models import Customer


class CustomerRepository:
    """Handles database operations related to the Customer entity."""
    @staticmethod
    def create_customer(session, customer):
        """Create a new customer in data base."""
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    @staticmethod
    def update_customer(session, customer_id, data):
        """Update an existing customer in database."""
        customer = session.get(Customer, customer_id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
        return customer

    @staticmethod
    def delete_customer(session, customer_id):
        """Delete a customer frome database."""
        customer = session.get(Customer, customer_id)
        session.delete(customer)
        return customer

    @staticmethod
    def get_customer_by_id(session, customer_id):
        """Get customer from database with its ID."""
        return session.get(Customer, customer_id)

    @staticmethod
    def get_customer_by_email(session, customer_email):
        """Get customer from database with its email."""
        return session.query(Customer).filter_by(email=customer_email).first()

    @staticmethod
    def get_customer_by_company_name(session, company_name):
        """Get customer from database with its company name."""
        return session.query(Customer).filter_by(
            company_name=company_name).first()

    @staticmethod
    def get_customer_by_phone(session, phone):
        """Get customer from database with its phone number."""
        return session.query(Customer).filter_by(phone=phone).first()

    @staticmethod
    def get_all_customers(session):
        """Get all customers from database in a list."""
        return session.query(Customer).all()

    @staticmethod
    def get_customers_by_sales_id(session, sales_contact_id):
        """Retrieves all customers managed by a specific sales."""
        return session.query(Customer).filter_by(
            sales_contact_id=sales_contact_id).all()

    @staticmethod
    def get_customers_without_sales_contact(session):
        """Get all customers that have no sales contact assigned."""
        return session.query(Customer).filter(
            Customer.sales_contact_id.is_(None)).all()
