from app.models import Customer, Contract, User


def test_create_contract(session):
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

    contract = Contract(
        id=1,
        customer_id=customer.id,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )
    session.add(contract)
    session.commit()

    assert session.get(Contract, 1) is not None
