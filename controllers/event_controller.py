from services.event_service import EventService
from controllers.base_controller import BaseController
from models.permission import EventPermission

class EventController(BaseController):
    """Controller for handling events."""
    
    service = EventService
    permission_class = EventPermission
