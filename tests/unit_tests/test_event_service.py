from models.event import Event
from services.event_service import EventService
from repository.event_repository import EventRepository


def test_delete_event_success(mock_session, mocker):
    """Test la suppression réussie d'un événement."""
    fake_event = Event(
        id=1, contract_id=5, start_date="2024-06-01", location="Paris")

    mocker.patch.object(
        EventRepository, "get_event_by_id", return_value=fake_event)
    mocker.patch.object(
        EventRepository, "delete_event", return_value=fake_event)

    deleted_event = EventService.delete_event(mock_session, 1)

    assert deleted_event == fake_event
