from services.customer_service import CustomerService
from models.auth import auth_required
from models.permission import CustomerPermission, permission_required
from views.customer_view import CustomerView


class CustomerController:
    """Controller for handling customers."""

    def __init__(self):
        self.service = CustomerService
        self.permission_class = CustomerPermission

    @auth_required
    @permission_required("list_all")
    def list_all_customers(self, user_payload, session):
        """Displays all customers and offers an action."""
        while True:
            customers = self.service.list_all(session)
            customer_id = CustomerView.display_customers_and_get_choice(
                customers
            )

            if customer_id is None:
                break

            self.show_customer_details(session, customer_id)

    @auth_required
    @permission_required("list_my_customers")
    def list_my_customers(self, user_payload, session):
        """Displays customers assigned to the logged-in user."""
        while True:
            customers = self.service.list_by_sales_id(
                session, user_payload["id"]
            )
            customer_id = CustomerView.display_customers_and_get_choice(
                customers
            )

            if customer_id is None:
                break

            self.show_customer_details(session, customer_id)

    @auth_required
    @permission_required("get")
    def show_customer_details(self, user_payload, session, customer_id):
        """Displays customer details and offers update/deletion options."""
        customer = self.service.get_by_id(session, customer_id)
        if not customer:
            print("\n Customer not found.")
            return

        while True:
            choice = CustomerView.display_customer_details_and_get_choice(
                customer
            )

            if choice == "1":
                self.update_customer(session, customer_id)
            elif choice == "2":
                self.delete_customer(session, customer_id)
                break
            elif choice == "3":
                break
            else:
                print("\n Invalid choice, please try again.")

    @auth_required
    @permission_required("create")
    def create_customer(self, user_payload, session):
        """Creates a new customer."""
        customer_data = CustomerView.get_customer_creation_data()
        self.service.create(session, **customer_data)
        print("Customer successfully created.")

    @auth_required
    @permission_required("update", requires_object=True)
    def update_customer(self, user_payload, session, customer_id):
        """Updates an existing customer."""
        updated_data = CustomerView.get_customer_update_data()
        if updated_data:
            self.service.update(session, customer_id, updated_data)
            print(f"Customer {customer_id} successfully updated.")

    @auth_required
    @permission_required("delete", requires_object=True)
    def delete_customer(self, user_payload, session, customer_id):
        """Deletes a customer after confirmation."""
        confirm = input(
            f"Confirm deletion of customer {customer_id}? (y/n): "
        ).strip().lower()

        if confirm == "y":
            self.service.delete(session, customer_id)
            print(f"Customer {customer_id} successfully deleted.")
