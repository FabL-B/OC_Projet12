from unittest.mock import MagicMock
from app.models import Event
from app.repository.event_repository import EventRepository


def test_create_event():
    mock_session = MagicMock()
    event = Event(
        id=1,
        contract_id=1,
        support_contact_id=1,
        start_date="2025-02-20",
        end_date="2025-02-21",
        location="Paris",
        attendees=50,
        notes="Annual Event"
    )

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    created_event = EventRepository.create_event(mock_session, event)

    mock_session.add.assert_called_once_with(event)
    mock_session.commit.assert_called_once()
    assert created_event == event


def test_get_event_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = Event(
        id=1,
        contract_id=1,
        support_contact_id=1,
        start_date="2025-02-20",
        end_date="2025-02-21",
        location="Paris",
        attendees=50,
        notes="Annual Event"
    )

    retrieved_event = EventRepository.get_event_by_id(mock_session, 1)

    mock_session.get.assert_called_once_with(Event, 1)
    assert retrieved_event.location == "Paris"


def test_update_event():
    mock_session = MagicMock()
    event = Event(
        id=1,
        contract_id=1,
        support_contact_id=1,
        start_date="2025-02-20",
        end_date="2025-02-21",
        location="Paris",
        attendees=50,
        notes="Annual Event"
    )
    mock_session.get.return_value = event

    updated_data = {"location": "Marseille", "attendees": 30}
    updated_event = EventRepository.update_event(mock_session, 1, updated_data)

    mock_session.get.assert_called_once_with(Event, 1)
    assert updated_event.location == "Marseille"
    assert updated_event.attendees == 30


def test_delete_event():
    mock_session = MagicMock()
    event = Event(
        id=1,
        contract_id=1,
        support_contact_id=1,
        start_date="2025-02-20",
        end_date="2025-02-21",
        location="Paris",
        attendees=50,
        notes="Annual Event"
    )
    mock_session.get.return_value = event

    deleted_event = EventRepository.delete_event(mock_session, 1)

    mock_session.get.assert_called_once_with(Event, 1)
    mock_session.delete.assert_called_once_with(event)
    assert deleted_event == event
