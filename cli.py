"""Interface for Splitwise API using Typer"""

class Cli:
    """Command Line Interface for Splitwise API operations."""
    def __init__(self, data_access, external_services):
        self.data_access = data_access
        self.external_services = external_services
        self.description_width = 18
        self.value_width = 7

    @property
    def table_line(self) -> str:
        """Generate a table line with the given character"""
        return "+----" + "-" * (self.description_width + self.value_width) + "-+"

    def items_sum(self, items: list[dict[str, float]]) -> float:
        """Calculate the sum of the values in the items."""
        return sum(abs(float(item["value"])) for item in items)


def show_all_users(users: list[dict[str, str]]) -> None:
    """Show all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")


def show_user_debts(debts: list[dict[str, float]]) -> None:
    """Show all user debts from the last month"""
    cli = Cli(data_access=None, external_services=None)
    value_w = cli.value_width
    description_w = cli.description_width
    value_items_sum = cli.items_sum(debts)

    # Print the payment items
    print("Items:\n")
    print(cli.table_line)
    print(f"| {'Descrição': ^{description_w}}|  {'Valor': ^{value_w}} |")
    print(cli.table_line)
    for item in debts:
        # Format the item description and value
        print(
            f"| {item['description']: <{description_w}}"
            f"R$ {abs(item['value']): >{value_w}} |"
        )
    print(cli.table_line)
    print(f"| {'Total': <{description_w}}R$ {value_items_sum: >{value_w}} |")
    print(cli.table_line)
    print("\n")


def show_payment_link(payment_link: str, payment_items: list[dict[str, float]]) -> None:
    """Show payment link and items"""
    cli = Cli(data_access=None, external_services=None)
    value_items_sum = cli.items_sum(payment_items)
    value_w = cli.value_width
    description_w = cli.description_width

    # Print the payment link
    print(cli.table_line)
    print(f"\nPayment Link: {payment_link}\n")
    print(cli.table_line)

    # Print the payment items
    print("Items:\n")
    print(cli.table_line)
    print(f"| {'Description': ^{description_w}}|  {'Value': ^{value_w}} |")
    print(cli.table_line)
    for item in payment_items:
        # Format the item description and value
        print(f"| {item['description']: <{description_w}}R$ {item['value']: >{value_w}} |")
    print(cli.table_line)
    print(f"| {'Total': <{description_w}}R$ {value_items_sum: >{value_w}} |")
    print(cli.table_line)
    print("\n")


def show_created_payment(items: dict[str, str, str], title:str) -> None:
    """Show created payment details"""
    # logic to display the created payment details
    cli = Cli(data_access=None, external_services=None)
    print("Payment created successfully!")
    content_width = max(len(item['name']) for item in items)

    total_value = cli.items_sum(items)
    print(cli.table_line)
    print(f"| {title: ^{content_width+cli.value_width + 4}} |")
    print(cli.table_line)
    for item in items:
        print(f"| {item['name']: <{content_width}} R$ {item['value']: >{cli.value_width}} |")
    print(cli.table_line)
    print(f"| {'Total': <{content_width}} R$ {total_value: >{cli.value_width}} |")
    print(cli.table_line)
    print("\n")
