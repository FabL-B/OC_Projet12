from app.models.event import Event
from app.repository.event_repository import EventRepository


def test_create_event(mock_session):
    """Test the creation and saving of an event in the database."""
    event = Event(
        contract_id=10, support_contact_id=3, location="Paris",
        start_date="2025-01-01", end_date="2025-01-02",
        attendees=100, notes="Conference"
    )

    EventRepository.create_event(mock_session, event)

    assert mock_session.add.called
    assert mock_session.commit.called


def test_get_event_by_id(mock_session):
    """Test retrieving an event by ID."""
    event = Event(id=1, contract_id=10, support_contact_id=3, location="Paris")
    mock_session.get.return_value = event

    result = EventRepository.get_event_by_id(mock_session, 1)

    assert result == event


def test_delete_event(mock_session):
    """Test deleting an event from the database."""
    event = Event(id=1, contract_id=10, support_contact_id=3, location="Paris")
    mock_session.get.return_value = event

    result = EventRepository.delete_event(mock_session, 1)

    assert mock_session.delete.called
    assert mock_session.commit.called
    assert result == event
