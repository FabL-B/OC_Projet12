from app.controllers.event_controller import EventController
from app.models.event import Event


def test_create_event_success(session, mocker, create_users,
                              create_customer_contract):
    """
    Tests successful creation of an event.
    """
    _, support_user = create_users
    _, contract = create_customer_contract

    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    event_data = {
        "location": "Paris",
        "start_date": "2025-04-01",
        "end_date": "2025-04-01",
        "attendees": 5,
        "contract_id": contract.id,
        "support_contact_id": support_user.id,
        "notes": "Event in Paris"
    }
    mocker.patch(
        "app.controllers.event_controller.EventView.get_event_creation_data",
        return_value=event_data
    )

    controller = EventController()
    controller.create_event(session=session)

    created_event = session.query(Event).filter_by(location="Paris").first()
    assert created_event is not None


def test_update_event_success(session, mocker, create_event):
    """
    Tests successful update of an event.
    """
    user_payload = {"id": 2, "role": "Support"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    mocker.patch(
        "app.controllers.event_controller.EventView.get_event_update_data",
        return_value={"notes": "Updated notes", "location": "Nice"}
    )

    controller = EventController()
    controller.update_event(session=session, obj=create_event)

    updated_event = session.get(Event, create_event.id)
    assert updated_event.notes == "Updated notes"
    assert updated_event.location == "Nice"


def test_delete_event_success(session, mocker, create_event):
    """
    Tests successful deletion of an event.
    """
    user_payload = {"id": 1, "role": "Admin"}
    mocker.patch("app.auth.auth.Auth.is_authenticated",
                 return_value=user_payload)

    mocker.patch("builtins.input", return_value="y")

    controller = EventController()
    controller.delete_event(session=session, obj=create_event)

    assert session.get(Event, create_event.id) is None
