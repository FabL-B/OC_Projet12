from models import User, Customer


def test_user_customer_relationship(test_db, setup_test_data):
    """Test a User can be related to many Customers."""

    test_db, user_sales, _, _, _ = setup_test_data

    customer2 = Customer(
        name="Customer B",
        company_name="Company B",
        email="customerB@test.com",
        phone="987654321",
        sales_contact_id=user_sales.id
    )

    test_db.add(customer2)
    test_db.commit()

    retrieved_user = test_db.query(User).filter_by(id=user_sales.id).first()

    assert len(retrieved_user.customers) == 2
    assert retrieved_user.name == "Sales Doe"
    assert retrieved_user.customers[0].name == "Customer A"
    assert retrieved_user.customers[1].name == "Customer B"
