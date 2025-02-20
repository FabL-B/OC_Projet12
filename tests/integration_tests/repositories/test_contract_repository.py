from app.models import Customer, Contract, User


def test_create_contract(session_test):
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

    contract = Contract(
        id=1,
        customer_id=customer.id,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )
    session_test.add(contract)
    session_test.commit()

    assert session_test.get(Contract, 1) is not None
