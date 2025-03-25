from app.controllers.contract_controller import ContractController
from app.models.contract import Contract


def test_create_contract_success(session, mocker, create_customer_contract):
    """
    Tests successful creation of a contract.
    """
    customer, _ = create_customer_contract

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    contract_data = {
        "customer_id": customer.id,
        "amount": 12345,
        "amount_due": 3000,
        "status": "unsigned"
    }
    mocker.patch(
        "app.views.contract_view.ContractView.get_contract_creation_data",
        return_value=contract_data
    )

    controller = ContractController()
    controller.create_contract(session=session)

    created_contract = session.query(
        Contract).order_by(Contract.id.desc()).first()
    assert created_contract is not None
    assert created_contract.amount == 12345
    assert created_contract.status == "unsigned"


def test_update_contract_success(session, mocker, create_customer_contract):
    """
    Tests successful update of a contract.
    """
    _, contract = create_customer_contract

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    mocker.patch(
        "app.views.contract_view.ContractView.get_contract_update_data",
        return_value={
            "amount_due": 0,
            "status": "signed"
        }
    )

    controller = ContractController()
    controller.update_contract(session=session, obj=contract)

    updated = session.get(Contract, contract.id)
    assert updated.amount_due == 0
    assert updated.status == "signed"


def test_delete_contract_success(session, mocker, create_customer_contract):
    """
    Tests successful deletion of a contract.
    """
    _, contract = create_customer_contract

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    mocker.patch("builtins.input", return_value="y")

    controller = ContractController()
    controller.delete_contract(session=session, obj=contract)

    assert session.get(Contract, contract.id) is None
