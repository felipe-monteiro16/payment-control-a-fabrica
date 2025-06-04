"""Interface for Splitwise API using Typer"""


def show_all_users(users: list[dict[str, str]]) -> None:
    """Show all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")


def show_user_debts(debts: list[dict[str, float]]) -> None:
    """Show all user debts from the last month"""
    if(not debts):
        print("No debts found for the user.\n")
        return

    description_width = 20
    value_width = 8
    value_items_sum = sum(abs(item["value"]) for item in debts)


    def generate_table_line(char: str) -> str:
        """Generate a table line with the given character"""
        return "+----" + char * (description_width + value_width) + "-+"


    # Print the payment items
    print("Items:\n")
    print(generate_table_line("-"))
    print(f"| {'Description': ^{description_width}}|  {'Value': ^{value_width}} |")
    print(generate_table_line("-"))
    for item in debts:
        # Format the item description and value
        print(f"| {item['description']: <{description_width}}R$ {abs(item['value']): >{value_width}} |")
    print(generate_table_line("-"))
    print(f"| {'Total': <{description_width}}R$ {value_items_sum: >{value_width}} |")
    print(generate_table_line("-"))
    print("\n")


def show_payment_link(payment_link: str, payment_items: list[dict[str, float]]) -> None:
    """Show payment link and items"""
    description_width = 20
    value_width = 8
    value_items_sum = sum(abs(item["value"]) for item in payment_items)


    def generate_table_line(char: str) -> str:
        """Generate a table line with the given character"""
        return "+----" + char * (description_width + value_width) + "-+"


    # Print the payment link
    print(generate_table_line("-"))
    print(f"\nPayment Link: {payment_link}\n")
    print(generate_table_line("-"))

    # Print the payment items
    print("Items:\n")
    print(generate_table_line("-"))
    print(f"| {'Description': ^{description_width}}|  {'Value': ^{value_width}} |")
    print(generate_table_line("-"))
    for item in payment_items:
        # Format the item description and value
        print(f"| {item['description']: <{description_width}}R$ {item['value']: >{value_width}} |")
    print(generate_table_line("-"))
    print(f"| {'Total': <{description_width}}R$ {value_items_sum: >{value_width}} |")
    print(generate_table_line("-"))
    print("\n")
