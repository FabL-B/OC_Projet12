from datetime import datetime

from models import Contract, Event


def test_contract_event_relationship(test_db, setup_test_data):
    """Test a Contract can be related to many Events."""

    test_db, _, user_support, _, contract = setup_test_data

    event1 = Event(
        contract_id=contract.id,
        support_contact_id=user_support.id,
        start_date=datetime(2025, 3, 1, 14, 0),
        end_date=datetime(2025, 3, 1, 18, 0),
        location="Vallet",
        attendees=30,
        notes="Muscadet event"
    )
    event2 = Event(
        contract_id=contract.id,
        support_contact_id=user_support.id,
        start_date=datetime(2025, 3, 1, 14, 0),
        end_date=datetime(2025, 3, 1, 18, 0),
        location="Nantes",
        attendees=50,
        notes="Nantes event"
    )

    test_db.add_all([event1, event2])
    test_db.commit()

    retrieved_contract = test_db.query(Contract).filter_by(
        id=contract.id).first()

    assert len(retrieved_contract.events) == 2
    assert retrieved_contract.events[0].location == "Vallet"
    assert retrieved_contract.events[1].location == "Nantes"
