import pytest
from unittest.mock import MagicMock, patch
from app.controllers.user_controller import UserController
from app.controllers.customer_controller import CustomerController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController


def test_create_contract(disable_auth_and_permissions):
    mock_service = MagicMock()
    mock_service.create.return_value = {"id": 1, "amount": 5000}
    controller = ContractController()
    controller.service = mock_service
    
    session_mock = MagicMock()
    
    with patch("app.views.contract_view.ContractView.get_contract_creation_data", return_value={"customer_id": 1, "amount": 5000, "amount_due": 2000, "status": "unsigned"}):
        controller.create_contract(session_mock)
    
    mock_service.create.assert_called_once()
