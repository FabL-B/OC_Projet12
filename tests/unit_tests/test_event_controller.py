import pytest
from models.event import Event
from controllers.event_controller import EventController
from services.event_service import EventService
from models.auth import Auth
from models.permission import EventPermission


@pytest.fixture
def event_controller():
    """Fixture to instantiate EventController."""
    return EventController()


def test_list_all_events(mocker, event_controller, mock_session):
    """Test retrieving all events."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        EventService,
        "list_all",
        return_value=[
            Event(
                id=1, contract_id=10, location="Paris", support_contact_id=3),
            Event(
                id=2, contract_id=11, location="Lyon", support_contact_id=5),
        ],
    )

    events = event_controller.list_all(mock_session)

    assert len(events) == 2
    assert events[0].location == "Paris"
    assert events[1].location == "Lyon"
    EventService.list_all.assert_called_once_with(mock_session)


def test_get_event(mocker, event_controller, mock_session):
    """Test retrieving a specific event."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        EventService,
        "get_by_id",
        return_value=Event(
            id=1, contract_id=10, location="Paris", support_contact_id=3
        ),
    )

    event = event_controller.get(mock_session, entity_id=1)

    assert event.location == "Paris"
    EventService.get_by_id.assert_called_once_with(mock_session, 1)


def test_create_event(mocker, event_controller, mock_session):
    """Test creating an event."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        EventPermission,
        "has_permission",
        return_value=True,
    )
    mocker.patch.object(
        EventService,
        "create",
        return_value=Event(
            id=1, contract_id=10, location="Paris", support_contact_id=3
        ),
    )

    event_controller.create(
        mock_session,
        contract_id=10,
        support_contact_id=3,
        start_date="2025-01-01",
        end_date="2025-01-02",
        location="Paris",
        attendees=100,
        notes="Annual conference",
    )

    EventService.create.assert_called_once_with(
        mock_session,
        contract_id=10,
        support_contact_id=3,
        start_date="2025-01-01",
        end_date="2025-01-02",
        location="Paris",
        attendees=100,
        notes="Annual conference",
    )


def test_update_event(mocker, event_controller, mock_session):
    """Test updating an event."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(EventService, "update", return_value=True)

    success = event_controller.update(
        mock_session, entity_id=1, data={"location": "Bordeaux"}
    )

    assert success is True
    EventService.update.assert_called_once_with(
        mock_session, 1, {"location": "Bordeaux"}
    )


def test_delete_event(mocker, event_controller, mock_session):
    """Test deleting an event."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(EventService, "delete", return_value=True)

    success = event_controller.delete(mock_session, entity_id=1)

    assert success is True
    EventService.delete.assert_called_once_with(mock_session, 1)
