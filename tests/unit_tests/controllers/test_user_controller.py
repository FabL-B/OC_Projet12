import pytest
from unittest.mock import MagicMock, patch
from app.controllers.user_controller import UserController
from app.controllers.customer_controller import CustomerController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController

def test_create_user(disable_auth_and_permissions):
    mock_service = MagicMock()
    mock_service.create.return_value = {"id": 1, "name": "John Doe"}
    controller = UserController()
    controller.service = mock_service
    
    session_mock = MagicMock()
    
    with patch("app.views.user_view.UserView.get_user_creation_data", return_value={"name": "John Doe", "email": "john@example.com", "password": "securepass", "role": "Sales"}):
        controller.create_user(session_mock)
    
    mock_service.create.assert_called_once()