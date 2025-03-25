from app.controllers.customer_controller import CustomerController
from app.models.customer import Customer


def test_create_customer_success(session, mocker, create_users):
    """
    Tests successful creation of a customer.
    """
    sales_user, _ = create_users
    user_payload = {"id": sales_user.id, "role": "Sales"}

    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    customer_data = {
        "name": "Client Test",
        "company_name": "Company Test",
        "email": "client@test.com",
        "phone": "0600000000"
    }
    mocker.patch(
        "app.views.customer_view.CustomerView.get_customer_creation_data",
        return_value=customer_data
    )

    controller = CustomerController()
    controller.create_customer(session=session)

    created_customer = session.query(
        Customer).order_by(Customer.id.desc()).first()
    assert created_customer is not None
    assert created_customer.name == "Client Test"
    assert created_customer.sales_contact_id == sales_user.id


def test_update_customer_success(session, mocker, create_customer_contract):
    """
    Tests successful update of a customer.
    """
    customer, _ = create_customer_contract

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    mocker.patch(
        "app.views.customer_view.CustomerView.get_customer_update_data",
        return_value={
            "email": "updated@email.com",
            "phone": "0707070707"
        }
    )

    controller = CustomerController()
    controller.update_customer(session=session, obj=customer)

    updated_customer = session.get(Customer, customer.id)
    assert updated_customer.email == "updated@email.com"
    assert updated_customer.phone == "0707070707"


def test_delete_customer_success(session, mocker, create_customer_contract):
    """
    Tests successful deletion of a customer.
    """
    customer, _ = create_customer_contract

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)
    mocker.patch("builtins.input", return_value="y")

    controller = CustomerController()
    controller.delete_customer(session=session, obj=customer)

    assert session.get(Customer, customer.id) is None
