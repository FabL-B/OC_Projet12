from sqlalchemy.orm import Session
from app.controllers.user_controller import UserController
from app.controllers.customer_controller import CustomerController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController
from app.views.app_view import AppView


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
        """Displays the User panel and dynamically manages actions."""
        while True:
            choice = AppView.show_user_menu()

            if choice == "1":
                self.user_controller.list_all_users(self.session)
            #Ajouter un list user par role
            elif choice == "2":
                self.user_controller.create_user(self.session)
            elif choice == "3":
                break
            else:
                print("\nInvalid choice, please try again.")

    def show_customer_panel(self):
        """Displays the Customer panel and dynamically manages actions."""
        while True:
            choice = AppView.show_customer_menu()

            if choice == "1":
                self.customer_controller.list_all_customers(self.session)
            elif choice == "2":
                self.customer_controller.list_my_customers(self.session)
            elif choice == "3":
                self.customer_controller.create_customer(self.session)
            elif choice == "4":
                break
            else:
                print("\nInvalid choice, please try again.")

    def show_contract_panel(self):
        """Displays the Contract panel and dynamically manages actions."""
        while True:
            choice = AppView.show_contract_menu()

            if choice == "1":
                self.contract_controller.list_all_contracts(self.session)
            elif choice == "2":
                self.contract_controller.list_unsigned_contracts(self.session)
            elif choice == "3":
                self.contract_controller.list_unpaid_contracts(self.session)
            elif choice == "4":
                self.contract_controller.create_contract(self.session)
            elif choice == "5":
                break
            else:
                print("\nInvalid choice, please try again.")

    def show_event_panel(self):
        """Displays the Event panel and dynamically manages actions."""
        while True:
            choice = AppView.show_event_menu()

            if choice == "1":
                self.event_controller.list_all_events(self.session)
            elif choice == "2":
                self.event_controller.list_my_events(self.session)
            elif choice == "3":
                self.event_controller.create_event(self.session)
            elif choice == "4":
                break
            else:
                print("\nInvalid choice, please try again.")

    def run(self):
        """Displays the main menu and dynamically handles navigation."""
        if not self.authenticate_user():
            return

        while True:
            choice = AppView.show_main_menu(self.main_menu)

            try:
                action = self.main_menu.get(choice)
                if action:
                    action_name, action_func = action
                    print(f"\nOpening: {action_name}...\n")
                    action_func()
                else:
                    print("\nInvalid choice, please try again.")
            except PermissionError as e:
                print(f"\nAccess Denied: {e}")
            except Exception as e:
                print(f"\nUnexpected Error: {e}")
