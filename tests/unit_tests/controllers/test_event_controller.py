import pytest
from unittest.mock import MagicMock, patch
from app.controllers.user_controller import UserController
from app.controllers.customer_controller import CustomerController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController
from app.permissions.permission import EventPermission, permission_required
from app.services.event_service import EventService
from app.views.event_view import EventView


def test_create_event(disable_auth_and_permissions):
    mock_service = MagicMock()
    mock_service.create.return_value = {"id": 1, "location": "Paris"}
    controller = EventController()
    controller.service = mock_service
    
    session_mock = MagicMock()
    
    with patch("app.views.event_view.EventView.get_event_creation_data", return_value={"contract_id": 1, "support_contact_id": 1, "start_date": "2025-02-20", "end_date": "2025-02-21", "location": "Paris", "attendees": 50, "notes": "Annual Event"}):
        controller.create_event(session_mock)
    
    mock_service.create.assert_called_once()

def test_list_my_events_without_user_payload(mocker):
    """Test que `list_my_events()` fonctionne sans user_payload."""
    mocker.patch.object(EventPermission, "user_id", 3)  # ✅ Simule un utilisateur connecté
    mocker.patch.object(EventService, "list_by_support_contact", return_value=[{"id": 1, "name": "Event 1"}])
    mocker.patch.object(EventView, "display_events_and_get_choice", return_value=None)

    class FakeEventController:
        permission_class = EventPermission
        service = EventService()

        @permission_required("list_my_events")
        def list_my_events(self, session):
            user_id = self.permission_class.user_id
            events = self.service.list_by_support_contact(session, user_id)
            return events

    controller = FakeEventController()
    session_mock = mocker.Mock()
    events = controller.list_my_events(session_mock)

    assert events == [{"id": 1, "name": "Event 1"}]