from app.services.customer_service import CustomerService
from app.auth.auth import auth_required
from app.permissions.permission import CustomerPermission, permission_required
from app.views.customer_view import CustomerView
from app.sentry.logger import sentry_log_exception, sentry_log_event


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
            print("\nCustomer not found.")
            return

        while True:
            choice = CustomerView.display_customer_details_and_get_choice(
                customer
            )

            if choice == "1":
                self.update_customer(session, obj=customer)
            elif choice == "2":
                self.delete_customer(session, obj=customer)
                break
            elif choice == "3":
                break
            else:
                print("\nInvalid choice, please try again.")

    @auth_required
    @permission_required("create")
    def create_customer(self, user_payload, session):
        """Creates a new customer."""
        try:
            customer_data = CustomerView.get_customer_creation_data()
            customer_data["sales_contact_id"] = user_payload["id"]
            self.service.create(session, **customer_data)
            print("Customer successfully created.")
            sentry_log_event(
                f"Created customer: {customer_data.get('name')}",
                level="info"
            )
        except Exception as e:
            sentry_log_exception(e)
            print("An error occurred during customer creation.")
            raise

    @auth_required
    @permission_required("update", requires_object=True)
    def update_customer(self, user_payload, session, **kwargs):
        """Updates an existing customer."""
        try:
            customer = kwargs.get("obj")
            updated_data = CustomerView.get_customer_update_data()
            if updated_data:
                self.service.update(session, customer.id, updated_data)
                print(f"Customer {customer.id} successfully updated.")
                sentry_log_event(
                    f"Updated customer {customer.id}", level="info"
                )
        except Exception as e:
            sentry_log_exception(e)
            print(f"An error occurred during updating customer {customer.id}.")
            raise

    @auth_required
    @permission_required("delete", requires_object=True)
    def delete_customer(self, user_payload, session, **kwargs):
        """Deletes a customer after confirmation."""
        try:
            customer = kwargs.get("obj")
            confirm = input(
                f"Confirm deletion of customer {customer.id}? (y/n): "
            ).strip().lower()
            if confirm == "y":
                self.service.delete(session, customer.id)
                print(f"Customer {customer.id} successfully deleted.")
                sentry_log_event(
                    f"Deleted customer {customer.id}", level="info"
                )
        except Exception as e:
            sentry_log_exception(e)
            print(
                f"An error occurred during deletion of customer {customer.id}."
            )
            raise
