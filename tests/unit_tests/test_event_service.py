from models.event import Event
from services.event_service import EventService
from repository.event_repository import EventRepository


def test_create_event_success(mock_session, mocker):
    """Test successful event creation."""
    mocker.patch.object(
        EventRepository,
        "get_event_by_id",
        return_value=None,
    )

    fake_event = Event(
        id=1, contract_id=101, support_contact_id=3, location="Paris"
    )
    mocker.patch.object(
        EventRepository,
        "create_event",
        return_value=fake_event,
    )

    event = EventService.create(
        mock_session,
        contract_id=101,
        support_contact_id=3,
        start_date="2025-01-01",
        end_date="2025-01-02",
        location="Paris",
        attendees=100,
        notes="Annual conference"
    )

    assert event.contract_id == 101
    assert event.location == "Paris"


def test_delete_event_success(mock_session, mocker):
    """Test successful event deletion."""
    fake_event = Event(
        id=1, contract_id=101, support_contact_id=3, location="Paris"
    )

    mocker.patch.object(
        EventRepository,
        "get_event_by_id",
        return_value=fake_event,
    )
    mocker.patch.object(
        EventRepository,
        "delete_event",
        return_value=fake_event,
    )

    deleted_event = EventService.delete(mock_session, 1)

    assert deleted_event == fake_event
