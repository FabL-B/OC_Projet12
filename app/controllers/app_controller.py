from sqlalchemy.orm import Session
from app.controllers.user_controller import UserController
from app.controllers.customer_controller import CustomerController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController
from app.views.app_view import AppView
from app.sentry.logger import sentry_log_exception


class AppController:
    """
    Main controller for managing the application and dynamically
    navigating between panels.
    """

    def __init__(self, session: Session):
        self.session = session
        self.user_controller = UserController()
        self.customer_controller = CustomerController()
        self.contract_controller = ContractController()
        self.event_controller = EventController()
        self.user_payload = None

        self.main_menu_actions = {
            "1": ("User Panel", self.show_user_panel),
            "2": ("Customer Panel", self.show_customer_panel),
            "3": ("Contract Panel", self.show_contract_panel),
            "4": ("Event Panel", self.show_event_panel),
            "5": ("Logout", self.logout),
        }

        self.user_menu_actions = {
            "1": self.user_controller.list_all_users,
            "2": self.user_controller.create_user,
            "3": None,
        }

        self.customer_menu_actions = {
            "1": self.customer_controller.list_all_customers,
            "2": self.customer_controller.list_my_customers,
            "3": self.customer_controller.list_customers_without_sales_contact,
            "4": self.customer_controller.create_customer,
            "5": None,
        }

        self.contract_menu_actions = {
            "1": self.contract_controller.list_all_contracts,
            "2": self.contract_controller.list_unsigned_contracts,
            "3": self.contract_controller.list_unpaid_contracts,
            "4": self.contract_controller.create_contract,
            "5": None,
        }

        self.event_menu_actions = {
            "1": self.event_controller.list_all_events,
            "2": self.event_controller.list_my_events,
            "3": self.event_controller.list_events_without_support_contact,
            "4": self.event_controller.create_event,
            "5": None,
        }

    def authenticate_user(self):
        """Handles user authentication."""
        email, password = AppView.get_login_credentials()
        tokens = self.user_controller.login_user(self.session, email, password)

        if tokens:
            self.user_payload = tokens["user"]
            print("\nLogin successful!")
            return True

        print("\nLogin failed. Please check your credentials.")
        return False

    def logout(self):
        """Logs out the user."""
        print("\nLogging out...")
        exit()

    def handle_menu(self, menu_view, menu_actions):
        """Handles dynamic menu navigation."""
        while True:
            choice = menu_view()
            action = menu_actions.get(choice)
            if action:
                action(self.session)
            elif action is None:
                return
            else:
                print("\nInvalid choice, please try again.")

    def show_user_panel(self):
        self.handle_menu(
            AppView.show_user_menu,
            self.user_menu_actions
        )

    def show_customer_panel(self):
        self.handle_menu(
            AppView.show_customer_menu,
            self.customer_menu_actions
        )

    def show_contract_panel(self):
        self.handle_menu(
            AppView.show_contract_menu,
            self.contract_menu_actions
        )

    def show_event_panel(self):
        self.handle_menu(
            AppView.show_event_menu,
            self.event_menu_actions
        )

    def run(self):
        """Displays the main menu and dynamically handles navigation."""
        if not self.authenticate_user():
            return

        while True:
            try:
                choice = AppView.show_main_menu(self.main_menu_actions)
                action = self.main_menu_actions.get(choice)
                if action:
                    _, action_func = action
                    action_func()
                else:
                    print("\nInvalid choice, please try again.")
            except PermissionError as e:
                print(f"\nAccess Denied: {e}")
            except Exception as e:
                sentry_log_exception(e)
                print(f"\nUnexpected Error: {e}")
