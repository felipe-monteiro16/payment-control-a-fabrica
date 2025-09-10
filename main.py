"""Splitwise API Python Client"""
import typer # type: ignore
from data_access import DataAccess
from external_services import ExternalServices
from cli import show_all_users, show_user_debts, show_payment_link, show_created_payment

app = typer.Typer()


@app.command()
def get_users() -> None:
    """Get all users from Splitwise API"""
    # Initialize the Data Access Layer
    data_access = DataAccess()

    # Get users from Splitwise API
    users = data_access.get_all_users()

    # Show users in the CLI
    show_all_users(users)



@app.command()
def get_user_debts(user_id: int) -> None:
    """Get user debts from the last month by ID."""
    # Initialize the Data Access Layer
    data_access = DataAccess()

    # Get user debts from Splitwise API
    user_debts = data_access.get_user_debts(user_id)

    # Show user debts in the CLI
    show_user_debts(user_debts)


@app.command()
def create_payment_link(user_id: int,) -> None:
    """Get the payment link for the given user_id."""
    # Initialize the Data Access Layer
    data_access = DataAccess()
    external_services = ExternalServices()

    # Create payment link
    user_debts = data_access.get_user_debts(user_id)
    payment_link, payment_items = external_services.create_payment_link(user_debts, user_id)

    # Show payment link in the CLI
    show_payment_link(payment_link, payment_items)


@app.command()
def send_payment_link(user_id: int) -> None:
    """Get user debts and payment link, then send them to the user."""
    # Initialize the Data Access Layer
    data_access = DataAccess()
    external_services = ExternalServices()

    # Create payment link
    user_debts = data_access.get_user_debts(user_id)
    payment_link, payment_items = external_services.create_payment_link(user_debts, user_id)

    # Send to the user
    user_contact = data_access.get_user_contact(user_id)
    external_services.send_debt_to_user(user_contact, payment_link, payment_items)

    # Show payment link in the CLI
    show_payment_link(payment_link, payment_items)


@app.command()
def create_user_debts(
    path: str = typer.Option(
        "data_access/src/debts.csv", "--path", "-p", help="Path to the CSV file with user debts."),
    description: str = typer.Option(
        ..., "--description", "-d", help="Description of the expense."
    )
) -> None:
    """Create user debts with Splitwise API."""
    # Initialize the Data Access Layer
    data_access = DataAccess()

    # Create user debts with Splitwise
    debts = data_access.get_debts_from_csv(csv_path=path)
    expenses, description = data_access.create_user_debts(path, description, debts)

    # Show created payment in the CLI
    show_created_payment(expenses, description)


@app.command()
def get_paid_debts():
    """Verify the paid users and send to Splitwise"""
    # Initialize the External Services and Data Access Layer
    external_services = ExternalServices()
    data_access = DataAccess()

    # Get paid users from external services
    paid_users = external_services.get_paid_debts()

    # Send payments to Splitwise API
    data_access.send_payments(paid_users)

if __name__ == "__main__":
    app()
