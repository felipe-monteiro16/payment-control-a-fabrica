"""Interface for Splitwise API using Typer"""


def show_all_users(users: list[dict[str, str]]) -> None:
    """Show all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")


def show_user_debts(debts: list[dict[str, str]]) -> None:
    """Show all user debts from the last month"""
    if not debts:
        print("No debts found.")
        return
    for debt in debts:
        print(f"Debt: {debt['name']} | Balance: {debt['balance']}")
