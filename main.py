"""Splitwise API Python Client"""
import typer
from data_access import DataAccess
from cli import show_all_users

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


if __name__ == "__main__":
    app()
