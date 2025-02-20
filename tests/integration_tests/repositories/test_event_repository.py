from app.models import User, Contract, Event, Customer


def test_create_event(session_test):
    user = User(
        id=30,
        name="Support P",
        email="support@example.com",
        role="Support"
    )
    user.set_password("supportpass")
    session_test.add(user)
    session_test.commit()

    sales_user = User(
        id=40,
        name="Sales P",
        email="sales@example.com",
        role="Sales"
    )
    sales_user.set_password("salespass")
    session_test.add(sales_user)
    session_test.commit()

    customer = Customer(
        id=2, name="Client D",
        company_name="Company D",
        email="clientD@example.com",
        phone="2223334444",
        sales_contact_id=sales_user.id
    )
    session_test.add(customer)
    session_test.commit()

    contract = Contract(
        id=1,
        customer_id=customer.id,
        amount=8000,
        amount_due=5000,
        status="signed"
    )
    session_test.add(contract)
    session_test.commit()

    event = Event(
        id=1,
        contract_id=contract.id,
        support_contact_id=user.id,
        start_date="2025-02-20",
        end_date="2025-02-21",
        location="Paris",
        attendees=50,
        notes="Annual Event"
    )
    session_test.add(event)
    session_test.commit()

    assert session_test.get(Event, 1) is not None
