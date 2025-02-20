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

    created_event = EventRepository.create_event(mock_session, event)

    mock_session.add.assert_called_once_with(event)
    mock_session.commit.assert_called_once()
    assert created_event == event


def test_get_event_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = Event(
        id=2,
        contract_id=1,
        support_contact_id=1,
        start_date="2025-02-22",
        end_date="2025-02-23",
        location="Lyon",
        attendees=100,
        notes="Conference"
    )

    retrieved_event = EventRepository.get_event_by_id(mock_session, 2)

    mock_session.get.assert_called_once_with(Event, 2)
    assert retrieved_event.location == "Lyon"
