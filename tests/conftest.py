import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from config.database import Base
from app.models.user import User
from app.models.customer import Customer
from app.models.contract import Contract
from app.models.event import Event


load_dotenv()
TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/epicevent_test_db"  # noqa: E501

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# ------------------------- DB session -------------------------


@pytest.fixture(scope="function")
def session():
    """Fixture that creates a temporary PostgreSQL database for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


# ------------------------- Data creation -------------------------


@pytest.fixture
def create_users(session):
    sales_user = User(
        role="Sales",
        name="Sales User",
        email="sales@test.com",
        password_hash="hashed"
    )
    support_user = User(
        role="Support",
        name="Support User",
        email="support@test.com",
        password_hash="hashed"
    )
    session.add_all([sales_user, support_user])
    session.commit()
    return sales_user, support_user


@pytest.fixture
def create_customer_contract(session, create_users):
    sales_user, _ = create_users
    customer = Customer(
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890",
        sales_contact_id=sales_user.id
    )
    contract = Contract(
        customer=customer,
        amount=5000,
        amount_due=2000,
        status="signed"
    )
    session.add_all([customer, contract])
    session.commit()
    return customer, contract


@pytest.fixture
def create_event(session, create_users, create_customer_contract):
    _, support_user = create_users
    _, contract = create_customer_contract
    event = Event(
        contract=contract,
        support_contact_id=support_user.id,
        location="Paris",
        start_date="2025-04-01",
        end_date="2025-04-01",
        attendees=10,
        notes="Initial notes"
    )
    session.add(event)
    session.commit()
    return event
