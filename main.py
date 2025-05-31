"""Splitwise API Python Client"""
import typer # type: ignore
from data_access import DataAccess
from cli import show_all_users, show_user_debts, show_payment_link

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
def get_payment_link(user_id: int,) -> None:
    """Get the payment link for the given user_id."""
    # Initialize the Data Access Layer
    data_access = DataAccess()

    # Create payment link
    user_debts = data_access.get_user_debts(user_id)
    payment_link, payment_items = data_access.get_payment_link(user_debts)

    # Show payment link in the CLI
    show_payment_link(payment_link, payment_items)

if __name__ == "__main__":
    #get_user_debts(30400274)
    app()
