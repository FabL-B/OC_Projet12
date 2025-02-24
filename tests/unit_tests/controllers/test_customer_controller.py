import pytest
from unittest.mock import MagicMock, patch
from app.controllers.user_controller import UserController
from app.controllers.customer_controller import CustomerController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController


def test_create_customer(disable_auth_and_permissions):
    mock_service = MagicMock()
    mock_service.create.return_value = {"id": 1, "name": "Client A"}
    controller = CustomerController()
    controller.service = mock_service
    
    session_mock = MagicMock()
    
    with patch("app.views.customer_view.CustomerView.get_customer_creation_data", return_value={"name": "Client A", "company_name": "Company A", "email": "client@example.com", "phone": "1234567890"}):
        controller.create_customer(session_mock)
    
    mock_service.create.assert_called_once()
