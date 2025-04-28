"""Splitwise API Python Client"""
import typer
from data_access import DataAccess
from cli import show_all_users, show_user_debts

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
    """Get all debts for a user"""
    # Initialize the Data Access Layer
    data_access = DataAccess()

    # Get user debts from Splitwise API
    user_debts = data_access.get_user_debts(user_id)

    # Show user debts in the CLI
    show_user_debts(user_debts)


if __name__ == "__main__":
    #get_user_debts(30400274)
    app()
