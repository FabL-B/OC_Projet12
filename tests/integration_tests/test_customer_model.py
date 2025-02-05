from models import Contract, Customer


def test_customer_contract_relationship(test_db, setup_test_data):
    """Test a Customer can be related to many Contracts."""

    test_db, _, _, customer, _ = setup_test_data

    contract2 = Contract(
        customer_id=customer.id,
        amount=10000,
        amount_due=5000,
        status="unsigned"
    )

    test_db.add(contract2)
    test_db.commit()

    retrieved_customer = test_db.query(Customer).filter_by(
        id=customer.id).first()

    # contracts[0] is set up in conftest.py
    assert retrieved_customer.contracts[0].amount == 5000
    assert retrieved_customer.contracts[1].amount == 10000
