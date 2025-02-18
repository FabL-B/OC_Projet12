from sqlalchemy.orm import Session
from controllers.user_controller import UserController
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from views.app_view import AppView


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

        # Main menu
        self.main_menu = {
            "1": ("User Panel", self.show_user_panel),
            "2": ("Customer Panel", self.show_customer_panel),
            "3": ("Contract Panel", self.show_contract_panel),
            "4": ("Event Panel", self.show_event_panel),
            "5": ("Logout", self.logout),
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

    def logout(self, *args):
        """Logs out the user."""
        print("\nLogging out...")
        exit()

    def show_user_panel(self):
        """Displays the user panel and dynamically manages actions."""
        while True:
            choice = AppView.show_user_menu()

            if choice == "1":
                self.user_controller.list_all_users(self.session)
            elif choice == "2":
                self.user_controller.create_user(self.session)
            else:
                print("\nInvalid choice, please try again.")

    def show_customer_panel(self):
        """Displays the customer panel (to be implemented)."""
        pass

    def show_contract_panel(self):
        """Displays the contract panel (to be implemented)."""
        pass

    def show_event_panel(self):
        """Displays the event panel (to be implemented)."""
        pass

    def run(self):
        """Displays the main menu and dynamically handles navigation."""
        if not self.authenticate_user():
            return

        while True:
            choice = AppView.show_main_menu(self.main_menu)

            action = self.main_menu.get(choice)
            if action:
                action_name, action_func = action
                print(f"\nOpening: {action_name}...\n")
                action_func()
            else:
                print("\nInvalid choice, please try again.")
