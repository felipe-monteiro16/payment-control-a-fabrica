"""Interface for Splitwise API using Typer"""


def show_all_users(users: list[dict[str, str]]) -> None:
    """Get all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")
