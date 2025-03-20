from unittest.mock import MagicMock, patch
from app.services.event_service import EventService
from app.models.event import Event


def test_get_event_by_id():
    """Test retrieving an event by its ID."""
    mock_session = MagicMock()
    mock_event = Event(id=1, contract_id=2, location="Paris")

    with patch(
        "app.repository.event_repository.EventRepository.get_event_by_id",
        return_value=mock_event
    ):
        event = EventService.get_by_id(mock_session, 1)

    assert event.id == 1
    assert event.location == "Paris"


def test_create_event():
    """Test creating a new event."""
    mock_session = MagicMock()
    mock_event = Event(id=2, contract_id=3, location="Lyon")

    with patch(
        "app.repository.event_repository.EventRepository.create_event",
        return_value=mock_event
    ):
        created_event = EventService.create(
            mock_session,
            3,
            1,
            "2025-03-01",
            "2025-03-02",
            "Lyon",
            100,
            "Conference"
        )

    assert created_event.location == "Lyon"


def test_update_event():
    """Test updating an existing event."""
    mock_session = MagicMock()
    mock_event = Event(id=3, contract_id=4, location="Nice")
    updated_event = Event(id=3, contract_id=4, location="Marseille")

    with patch(
        "app.repository.event_repository.EventRepository.get_event_by_id",
        return_value=mock_event
    ):
        with patch(
            "app.repository.event_repository.EventRepository.update_event",
            return_value=updated_event
        ):
            result = EventService.update(
                mock_session,
                3,
                {"location": "Marseille"}
            )

    assert result.location == "Marseille"


def test_delete_event():
    """Test deleting an event."""
    mock_session = MagicMock()

    with patch(
        "app.repository.event_repository.EventRepository.delete_event",
        return_value=True
    ):
        result = EventService.delete(mock_session, 4)

    assert result is True
