import pytest
from sqlalchemy.orm import Session
from config.database import Base, SessionLocal, engine
from app.models import User, Customer, Contract


@pytest.fixture(scope="function")
def test_db():
    """Fixture that creates a clean database before each test."""
    Base.metadata.create_all(engine)
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def setup_test_data(test_db):
    """Fixture that creates common test data."""

    # Setup users
    user_sales = User(
        name="Sales Doe",
        email="sales@example.com",
        password_hash="hashed_pwd",
        role="Sales"
    )

    user_support = User(
        name="Support Doe",
        email="support@example.com",
        password_hash="hashed_pwd",
        role="Support"
    )

    test_db.add_all([user_sales, user_support])
    test_db.commit()

    # Setup customer
    customer = Customer(
        name="Customer A",
        company_name="Company A",
        email="customerA@test.com",
        phone="123456789",
        sales_contact_id=user_sales.id
    )
    test_db.add(customer)
    test_db.commit()

    # Setup Contract
    contract = Contract(
        customer_id=customer.id,
        amount=5000,
        amount_due=2500,
        status="unsigned"
    )
    test_db.add(contract)
    test_db.commit()

    return test_db, user_sales, user_support, customer, contract


@pytest.fixture
def mock_session(mocker):
    """Fixture to mock an SQLAlchemy session."""
    return mocker.Mock(spec=Session)
