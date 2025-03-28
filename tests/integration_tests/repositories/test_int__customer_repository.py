from app.models import User, Customer


def test_create_customer(session):
    user = User(
        id=10,
        name="Sales Person",
        email="sales@example.com",
        role="Sales"
    )
    user.set_password("salespass")
    session.add(user)
    session.commit()
    customer = Customer(
        id=1,
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890",
        sales_contact_id=user.id
    )
    session.add(customer)
    session.commit()
    assert session.get(Customer, 1) is not None


def test_get_customer_by_id(session):
    user = User(
        id=20,
        name="Sales P2",
        email="sales2@example.com",
        role="Sales"
    )
    user.set_password("salespass")
    session.add(user)
    session.commit()

    customer = Customer(
        id=1,
        name="Client B",
        company_name="Company B",
        email="clientB@example.com",
        phone="9876543210",
        sales_contact_id=user.id
    )
    session.add(customer)
    session.commit()

    retrieved_customer = session.get(Customer, 1)
    assert retrieved_customer is not None
    assert retrieved_customer.company_name == "Company B"
