"""Interface for Splitwise API using Typer"""


def show_all_users(users: list[dict[str, str]]) -> None:
    """Show all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")


def show_user_debts(debts: list[dict[str, float]]) -> None:
    """Show all user debts from the last month"""
    if not debts:
        print("No debts found.")
        return
    for debt in debts:
        print(f"Debt: {debt['name']} | Balance: {debt['balance']}")


def show_payment_link(payment_link: str, payment_items: list[dict[str, float]]) -> None:
    """Show payment link and items"""
    print(f"Payment Link: {payment_link}")
    print("Items:")
    a = 15
    b = 8
    print("+-","-" * (a+b),"-+")
    print(f"| {'Description': ^15} | {'Value': ^8} |")
    print("+-","-" * (a+b),"-+")
    for item in payment_items:
        # Format the item description and value
        print(f"| {item['description']: <15}R$ {item['value']: >8} |")
    print("+-","-" * (a+b),"-+")