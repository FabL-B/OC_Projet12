import pytest
from app.controllers.app_controller import AppController
from app.models.user import User
from app.models.customer import Customer
from app.models.contract import Contract
from app.models.event import Event


def test_functional_create_update_delete_user(monkeypatch, session):
    """
    Functional test for user CRUD operations: create, update, delete.
    """
    admin_user = User(name="Admin", email="admin@example.com", role="Admin")
    admin_user.set_password("test")
    session.add(admin_user)
    session.commit()

    # --- PHASE 1: CREATE USER ---
    inputs_create = iter([
        "admin@example.com", "test",
        "1", "2",
        "Alice", "alice@example.com", "password123", "Support",
        "3", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_create))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_create))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    alice = session.query(User).filter_by(email="alice@example.com").first()
    assert alice is not None
    assert alice.name == "Alice"
    assert alice.role == "Support"

    # --- PHASE 2: UPDATE USER ---
    inputs_update = iter([
        "admin@example.com", "test",
        "1", "1", str(alice.id),
        "1",
        "Alice Updated", "updated@example.com", "Management",
        "3", " ", "3", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_update))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_update))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    updated_user = session.query(User).filter_by(
        email="updated@example.com").first()
    assert updated_user is not None
    assert updated_user.name == "Alice Updated"
    assert updated_user.role == "Management"

    # --- PHASE 3: DELETE USER ---
    inputs_delete = iter([
        "admin@example.com", "test",
        "1", "1", str(updated_user.id),
        "2", "y",
        "", "3", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_delete))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_delete))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    assert session.query(User).filter_by(
        email="updated@example.com").first() is None


def test_functional_create_update_delete_customer(monkeypatch, session):
    """
    Functional test for customer CRUD operations: create, update, delete.
    """
    user = User(name="Sales", email="test@example.com", role="Sales")
    user.set_password("test")
    session.add(user)
    session.commit()

    # --- PHASE 1: CREATE CUSTOMER ---
    inputs_create = iter([
        "test@example.com", "test",
        "2", "4",
        "John", "Corp", "john@example.com", "+33600000001",
        "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_create))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_create))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    customer = session.query(Customer).filter_by(
        email="john@example.com").first()
    assert customer is not None
    assert customer.name == "John"
    assert customer.company_name == "Corp"

    # --- PHASE 2: UPDATE CUSTOMER ---
    inputs_update = iter([
        "test@example.com", "test",
        "2", "1", str(customer.id),
        "1",
        "Johnny", "Corpx", "johnny@example.com", "+33600000002", "",
        "3", "", "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_update))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_update))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    updated_customer = session.query(Customer).filter_by(
        email="johnny@example.com").first()
    assert updated_customer is not None
    assert updated_customer.name == "Johnny"
    assert updated_customer.company_name == "Corpx"

    # --- PHASE 3: DELETE CUSTOMER ---
    inputs_delete = iter([
        "test@example.com", "test",
        "2", "1", str(updated_customer.id),
        "2", "y",
        "3", "", "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_delete))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_delete))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    assert session.query(Customer).filter_by(
        email="johnny@example.com").first() is None


def test_functional_create_update_delete_contract(monkeypatch, session):
    """
    Functional test for contract CRUD operations: create, update, delete.
    """
    user = User(name="Admin", email="test@example.com", role="Admin")
    user.set_password("test")
    session.add(user)
    session.commit()

    customer = Customer(
        name="Client", company_name="Corp", email="client@corp.com",
        phone="0600", sales_contact_id=user.id
    )
    session.add(customer)
    session.commit()

    # --- PHASE 1: CREATE CONTRACT ---
    inputs_create = iter([
        "test@example.com", "test",
        "3", "4", str(customer.id), "1000", "500", "unsigned",
        "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_create))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_create))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    created_contract = session.query(Contract).filter_by(amount=1000).first()
    assert created_contract is not None
    assert created_contract.status == "unsigned"
    assert created_contract.amount_due == 500

    # --- PHASE 2: UPDATE CONTRACT ---
    inputs_update = iter([
        "test@example.com", "test",
        "3", "3", "1", "1",
        "1001", "0", "signed",
        "3", "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_update))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_update))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    updated_contract = session.query(Contract).filter_by(amount=1001).first()
    assert updated_contract is not None
    assert updated_contract.status == "signed"
    assert updated_contract.amount_due == 0

    # --- PHASE 3: DELETE CONTRACT ---
    inputs_delete = iter([
        "test@example.com", "test",
        "3", "3", "1", "2", "y",
        "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_delete))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_delete))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    assert session.query(Contract).filter_by(amount=1001).first() is None


def test_functional_create_update_delete_event(monkeypatch, session):
    """
    Functional test for event CRUD operations: create, update, delete.
    """
    admin_user = User(name="Admin", email="admin@example.com", role="Admin")
    admin_user.set_password("test")

    sales_user = User(name="Sales", email="sales@example.com", role="Sales")
    sales_user.set_password("test")

    support_user = User(name="Support", email="support@example.com",
                        role="Support")
    support_user.set_password("test")

    session.add_all([admin_user, sales_user, support_user])
    session.commit()

    customer = Customer(
        name="Event Client", company_name="EventCorp",
        email="event@example.com", phone="+33700000001",
        sales_contact_id=sales_user.id
    )
    session.add(customer)
    session.commit()

    contract = Contract(
        customer_id=customer.id, amount=8000,
        amount_due=2000, status="signed"
    )
    session.add(contract)
    session.commit()

    # --- PHASE 1: CREATE EVENT ---
    inputs_create = iter([
        "admin@example.com", "test",
        "4", "4", str(contract.id), str(support_user.id),
        "2025-06-01", "2025-06-02", "Paris", "30", "Initial Event",
        "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_create))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_create))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    event = session.query(Event).filter_by(location="Paris").first()
    assert event is not None
    assert event.notes == "Initial Event"
    assert event.attendees == 30

    # --- PHASE 2: UPDATE EVENT ---
    inputs_update = iter([
        "admin@example.com", "test",
        "4", "1", str(event.id),
        "1",
        "2025-06-03", "2025-06-04", "Marseille", "35", "Updated notes",
        "3", "", "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_update))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_update))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    updated_event = session.query(Event).filter_by(
        location="Marseille").first()
    assert updated_event is not None
    assert updated_event.notes == "Updated notes"
    assert updated_event.attendees == 35

    # --- PHASE 3: DELETE EVENT ---
    inputs_delete = iter([
        "admin@example.com", "test",
        "4", "1", str(updated_event.id),
        "2", "y",
        "3", "", "5", "5"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_delete))
    monkeypatch.setattr("rich.prompt.Prompt.ask",
                        lambda *args, **kwargs: next(inputs_delete))

    with pytest.raises(SystemExit):
        AppController(session=session).run()

    assert session.query(Event).filter_by(
        id=updated_event.id).first() is None
