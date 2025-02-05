from models import Event

from datetime import datetime


def test_event_support_contact_relationship(test_db, setup_test_data):
    """Test an Event can be related to a support User."""

    test_db, _, user_support, _, contract = setup_test_data

    event = Event(
        contract_id=contract.id,
        support_contact_id=user_support.id,
        start_date=datetime(2025, 3, 1, 14, 0),
        end_date=datetime(2025, 3, 1, 18, 0),
        location="Vallet",
        attendees=30,
        notes="Muscadet event"
    )

    test_db.add(event)
    test_db.commit()

    retrieved_event = test_db.query(Event).filter_by(id=event.id).first()

    assert retrieved_event.support_contact.name == "Support Doe"
    assert retrieved_event.support_contact.role == "Support"
