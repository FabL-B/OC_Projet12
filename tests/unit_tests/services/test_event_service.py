import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.repository.event_repository import EventRepository
from app.models.event import Event
from app.services.event_service import EventService

class TestEventService(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock(spec=Session)
        self.event_data = {
            "contract_id": 1,
            "support_contact_id": 2,
            "start_date": "2024-03-15",  # Use appropriate date/datetime format
            "end_date": "2024-03-17",
            "location": "Test Location",
            "attendees": 50,
            "notes": "Test Notes"
        }

    def test_get_by_id(self):
        mock_event = MagicMock(spec=Event)
        EventRepository.get_event_by_id = MagicMock(return_value=mock_event)
        event = EventService.get_by_id(self.session_mock, 1)
        self.assertEqual(event, mock_event)
        EventRepository.get_event_by_id.assert_called_once_with(self.session_mock, 1)

    def test_get_by_id_not_found(self):
        EventRepository.get_event_by_id = MagicMock(return_value=None)
        with self.assertRaises(ValueError) as context:
            EventService.get_by_id(self.session_mock, 1)
        self.assertEqual(str(context.exception), "Event not found.")

    def test_list_all(self):
        mock_events = [
            Event(id=1, start_date="2024-03-10", end_date="2024-03-12", location="Loc 1"),
            Event(id=2, start_date="2024-03-15", end_date="2024-03-17", location="Loc 2"),
        ]
        EventRepository.get_all_events = MagicMock(return_value=mock_events)
        events = EventService.list_all(self.session_mock)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["id"], 1)
        EventRepository.get_all_events.assert_called_once_with(self.session_mock)

    def test_list_by_support_contact(self):
        mock_events = [
            Event(id=1, start_date="2024-03-10", end_date="2024-03-12", location="Loc 1", support_contact_id=1),
        ]
        EventRepository.get_events_by_support_contact = MagicMock(return_value=mock_events)
        events = EventService.list_by_support_contact(self.session_mock, 1)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], 1)
        EventRepository.get_events_by_support_contact.assert_called_once_with(self.session_mock, 1)

    @patch("app.services.event_service.EventRepository.create_event")
    def test_create(self, mock_create_event):
        mock_event = MagicMock(spec=Event)
        mock_create_event.return_value = mock_event
        event = EventService.create(self.session_mock, self.event_data["contract_id"], self.event_data["support_contact_id"],
                                    self.event_data["start_date"], self.event_data["end_date"], self.event_data["location"],
                                    self.event_data["attendees"], self.event_data["notes"])
        self.assertEqual(event, mock_event)
        mock_create_event.assert_called_once()

    @patch("app.services.event_service.EventRepository.get_event_by_id")
    @patch("app.services.event_service.EventRepository.update_event")
    def test_update(self, mock_update_event, mock_get_event_by_id):
        mock_event = MagicMock(spec=Event)
        mock_get_event_by_id.return_value = mock_event
        updated_data = {"location": "Updated Location"}
        updated_event = EventService.update(self.session_mock, 1, updated_data)
        self.assertEqual(updated_event, mock_update_event.return_value) # or mock_event if update returns the object
        mock_get_event_by_id.assert_called_once_with(self.session_mock, 1)
        mock_update_event.assert_called_once_with(self.session_mock, 1, updated_data)

    @patch("app.services.event_service.EventRepository.get_event_by_id")
    def test_update_event_not_found(self, mock_get_event_by_id):
        mock_get_event_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            EventService.update(self.session_mock, 1, {"location": "Updated Location"})
        self.assertEqual(str(context.exception), "Event not found.")

    @patch("app.services.event_service.EventRepository.get_event_by_id")
    @patch("app.services.event_service.EventRepository.delete_event")
    def test_delete(self, mock_delete_event, mock_get_event_by_id):
        mock_event = MagicMock(spec=Event)
        mock_get_event_by_id.return_value = mock_event
        deleted = EventService.delete(self.session_mock, 1)
        self.assertEqual(deleted, mock_delete_event.return_value) # or True if delete returns a boolean
        mock_get_event_by_id.assert_called_once_with(self.session_mock, 1)
        mock_delete_event.assert_called_once_with(self.session_mock, 1)

    @patch("app.services.event_service.EventRepository.get_event_by_id")
    def test_delete_event_not_found(self, mock_get_event_by_id):
        mock_get_event_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            EventService.delete(self.session_mock, 1)
        self.assertEqual(str(context.exception), "Event not found.")

if __name__ == '__main__':
    unittest.main()