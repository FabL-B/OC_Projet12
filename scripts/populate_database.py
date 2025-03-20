import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import SessionLocal  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.customer import Customer  # noqa: E402
from app.models.contract import Contract  # noqa: E402
from app.models.event import Event  # noqa: E402


def seed_data():
    """Inserts test data into the database."""
    session = SessionLocal()

    # Creating users
    users = {
        "management": User(
            name="management", email="management@test.com", role="Management"),
        "sales1": User(
            name="sales1", email="sales1@test.com", role="Sales"),
        "sales2": User(
            name="sales2", email="sales2@test.com", role="Sales"),
        "support1": User(
            name="support1", email="support1@test.com", role="Support"),
        "support2": User(
            name="support2", email="support2@test.com", role="Support"),
    }

    # Setting passwords
    for user in users.values():
        user.set_password("test")
        session.add(user)

    session.commit()
    print("Users test data successfully inserted.")

    # Creating customers
    customers = {
        "customer1": Customer(
            name="customer1", company_name="customer1",
            email="customer1@test.com", phone="+1234567890",
            sales_contact_id=users["sales1"].id
        ),
        "customer2": Customer(
            name="customer2", company_name="customer2",
            email="customer2@test.com", phone="+2345678901",
            sales_contact_id=users["sales2"].id
        )
    }

    for customer in customers.values():
        session.add(customer)

    session.commit()
    print("Customers test data successfully inserted.")

    # Creating contracts
    contracts = {
        "contract1": Contract(
            customer_id=customers["customer1"].id,
            amount=1000.0, amount_due=1000.0, status="unsigned"
        ),
        "contract2": Contract(
            customer_id=customers["customer1"].id,
            amount=2000.0, amount_due=100.0, status="signed"
        ),
        "contract3": Contract(
            customer_id=customers["customer2"].id,
            amount=10000.0, amount_due=1000.0, status="signed"
        )
    }

    for contract in contracts.values():
        session.add(contract)

    session.commit()
    print("Contracts test data successfully inserted.")

    # Creating events
    events = [
        Event(
            contract_id=contracts["contract2"].id,
            support_contact_id=users["support1"].id,
            start_date="2025-04-21", end_date="2025-04-26",
            location="Vallet", attendees=30, notes="Event in Vallet"
        ),
        Event(
            contract_id=contracts["contract2"].id,
            support_contact_id=None,
            start_date="2025-04-21", end_date="2025-04-26",
            location="Nantes", attendees=50, notes="Event in Nantes"
        )
    ]

    for event in events:
        session.add(event)

    session.commit()
    print("Events test data successfully inserted.")

    session.close()


if __name__ == "__main__":
    seed_data()
