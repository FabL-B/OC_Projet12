from app.models import User, Customer


def test_create_customer(session_test):
    user = User(
        id=10,
        name="Sales Person",
        email="sales@example.com",
        role="Sales"
    )
    user.set_password("salespass")
    session_test.add(user)
    session_test.commit()
    customer = Customer(
        id=1,
        name="Client A",
        company_name="Company A",
        email="client@example.com",
        phone="1234567890",
        sales_contact_id=user.id
    )
    session_test.add(customer)
    session_test.commit()
    assert session_test.get(Customer, 1) is not None


def test_get_customer_by_id(session_test):
    user = User(
        id=20,
        name="Sales P2",
        email="sales2@example.com",
        role="Sales"
    )
    user.set_password("salespass")
    session_test.add(user)
    session_test.commit()

    customer = Customer(
        id=1,
        name="Client B",
        company_name="Company B",
        email="clientB@example.com",
        phone="9876543210",
        sales_contact_id=user.id
    )
    session_test.add(customer)
    session_test.commit()

    retrieved_customer = session_test.get(Customer, 1)
    assert retrieved_customer is not None
    assert retrieved_customer.company_name == "Company B"
