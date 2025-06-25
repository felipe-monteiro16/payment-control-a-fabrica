"""Interface for Splitwise API using Typer"""
from dataclasses import dataclass
from datetime import datetime, timezone


def get_current_month() -> str:
    """Get the current month in the format 'MM/YY'."""
    return datetime.now(timezone.utc).strftime("%m/%y")

@dataclass
class Debt:
    """Class to represent user debt."""
    description: str
    value: float

    @property
    def full_description(self) -> str:
        """Get the description of the debt."""
        # Format the description with the value and date
        return f"{self.description} - {get_current_month()}"


@dataclass
class Cli:
    """Command Line Interface for Splitwise API operations."""
    def __init__(self, debts: list[dict[str, float]] = None):
        # Set default widths
        self.description_width = 18
        self.value_width = 7
        self.full_width = self.description_width + self.value_width + 3  # 3 for " R$"

        # Initialize user debts
        if debts:
            self.user_debts = [
                Debt(
                    item["description"].split()[0].capitalize(),
                    float(item['value'])  # Format value to Brazilian currency style
                )
                for item in debts
            ]
        else:
            self.user_debts = []


    def get_widths(self) -> tuple[int, int]:
        """Get the widths of the description and value columns."""
        if not self.user_debts:
            return self.description_width, self.value_width, self.full_width

        # Calculate the minimum widths based on the longest description and value
        self.description_width = max(
            len(item.description)
            for item in self.user_debts
        )

        self.value_width = len("9999,99")  # Fixed width for value column

        self.full_width = self.description_width + self.value_width + 3  # 3 for " R$"
        return self.description_width, self.value_width, self.full_width


    @property
    def table_line(self) -> str:
        """Generate a table line with the given character"""
        # Description width + Value width + 3 of the fixed string " R$"
        return "-" * self.full_width


    def items_sum(self) -> float:
        """Calculate the sum of the values in the items."""
        return sum(item.value for item in self.user_debts)


def show_all_users(users: list[dict[str, str]]) -> None:
    """Show all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")


def show_user_debts(debts: list[dict[str, float]]) -> None:
    """Show all user debts from the last month"""
    cli = Cli(debts)
    debts = cli.user_debts
    description_w, value_w, full_w = cli.get_widths()
    value_items_sum = cli.items_sum()

    # Print the payment items
    print("Items:\n")
    print(f"{f'RESUMO - {get_current_month()}': ^{full_w}}")
    print(cli.table_line)
    for item in debts:
        # Print the item with aligned description and value
        print(
            f"{item.description: <{description_w}} "
            f"R${item.value: >{value_w}.2f}"
        )
    print(cli.table_line)
    print(f"{'Total': <{description_w}} R${value_items_sum: >{value_w}.2f}")
    print("\n")


def show_payment_link(payment_link: str, user_debts: list[dict[str, float]]) -> None:
    """Show payment link and items"""
    cli = Cli(user_debts)
    user_debts = cli.user_debts
    value_items_sum = cli.items_sum()
    description_w, value_w, full_w = cli.get_widths()

    # Print the payment link
    print(cli.table_line)
    print(f"\nPayment Link: {payment_link}\n")
    print(cli.table_line)

    # Print the payment items
    print("Items:\n")
    print(f"{f'RESUMO - {get_current_month()}': ^{full_w}}")
    print(cli.table_line)
    for item in user_debts:
        # Print the item with aligned description and value
        print(
            f"{item.description: <{description_w}} "
            f"R${item.value: >{value_w}.2f}"
        )
    print(cli.table_line)
    print(f"{'Total': <{description_w}} R${value_items_sum: >{value_w}.2f}")
    print("\n")


def show_created_payment(items: dict[str, str, str], title:str) -> None:
    """Show created payment details"""
    # logic to display the created payment details
    cli = Cli(items)
    print("Payment created successfully!")
    content_width = max(len(item['name']) for item in items)

    total_value = cli.items_sum()
    print(cli.table_line)
    print(f"| {title: ^{content_width+cli.value_width + 4}} |")
    print(cli.table_line)
    for item in items:
        print(f"| {item['name']: <{content_width}} R$ {item['value']: >{cli.value_width}.2f} |")
    print(cli.table_line)
    print(f"| {'Total': <{content_width}} R$ {total_value: >{cli.value_width}.2f} |")
    print(cli.table_line)
    print("\n")
