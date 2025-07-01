"""Interface for Splitwise API using Typer"""
from data_classes import Debt, ExpenseDebt, get_current_month


class Cli:
    """Command Line Interface for Splitwise API operations."""
    expense_debts: list[Debt] = []
    expense_debts: list[ExpenseDebt] = []


    def __init__(self):
        # Set default widths
        self.label_width = 18
        self.value_width = 7
        self.full_width = self.label_width + self.value_width + 3  # 3 for " R$"


    def process_debts(self, debts: list[Debt]) -> None:
        """Convert a list of Debt objects to a list of Debt objects."""
        # Initialize user debts
        if debts:
            self.expense_debts = [
                Debt(
                    label=item.label.split()[0].capitalize(),
                    value=float(item.value)  # Format value to Brazilian currency style
                )
                for item in debts
            ]
        else:
            self.expense_debts = []


    def process_expense_debts(self, expenses: list[ExpenseDebt]) -> None:
        """Test"""
        # Initialize expense debts
        if expenses:
            self.expense_debts = expenses
        else:
            self.expense_debts = []


    def get_widths(self, title = None) -> tuple[int, int]:
        """Get the widths of the label and value columns."""
        if not self.expense_debts and not self.expense_debts:
            return self.label_width, self.value_width, self.full_width

        # Calculate the minimum widths based on the longest label and value
        self.label_width = max(
            len(item.label)
            for item in self.expense_debts
        )

        self.value_width = len("9999,99")  # Fixed width for value column

        self.full_width = self.label_width + self.value_width + 4  # 4 for " R$ "
        if title and len(title) > self.full_width:
            self.full_width = len(title) + 4
        return self.label_width, self.value_width, self.full_width


    def table_line(self, full_width=None) -> str:
        """Generate a table line with the given character"""
        # Label width + Value width + 4 of the fixed string " R$ "
        return "-" * (full_width if full_width else self.full_width)


    def items_sum(self) -> float:
        """Calculate the sum of the values in the items."""
        return sum(item.value for item in self.expense_debts)


def show_all_users(users: list[dict[str, str]]) -> None:
    """Show all users from Splitwise API"""
    for user in users:
        print(f"User ID: {user['id']} | Name: {user['first_name']} {user['last_name']}")


def show_user_debts(debts: list[dict[str, float]]) -> None:
    """Show all user debts from the last month"""
    cli = Cli()
    # Process the debts and calculate widths
    cli.process_debts(debts)
    label_w, value_w, full_w = cli.get_widths()
    value_items_sum = cli.items_sum()

    # Print the payment items
    print("Items:\n")
    print(f"{f'RESUMO - {get_current_month()}': ^{full_w}}")
    print(cli.table_line())
    for item in cli.expense_debts:
        # Print the item with aligned label and value
        print(
            f"{item.label: <{label_w}} "
            f"R${item.value: >{value_w}.2f}"
        )
    print(cli.table_line())
    print(f"{'Total': <{label_w}} R${value_items_sum: >{value_w}.2f}")
    print("\n")


def show_payment_link(payment_link: str, user_debts: list[dict[str, float]]) -> None:
    """Show payment link and items"""
    cli = Cli()
    cli.process_debts(user_debts)
    value_items_sum = cli.items_sum()
    label_w, value_w, full_w = cli.get_widths()

    # Print the payment link
    print(cli.table_line())
    print(f"\nPayment Link: {payment_link}\n")
    print(cli.table_line())

    # Print the payment items
    print("Items:\n")
    print(f"{f'RESUMO - {get_current_month()}': ^{full_w}}")
    print(cli.table_line())
    for item in cli.expense_debts:
        # Print the item with aligned label and value
        print(
            f"{item.label: <{label_w}} "
            f"R${item.value: >{value_w}.2f}"
        )
    print(cli.table_line())
    print(f"{'Total': <{label_w}} R${value_items_sum: >{value_w}.2f}")
    print("\n")


def show_created_payment(expense_debts: list[ExpenseDebt], title: str) -> None:
    """Show created payment details"""
    # logic to display the created payment details
    if not expense_debts:
        print("No items to display.")
        return
    cli = Cli()
    cli.process_expense_debts(expense_debts)
    #get the widths for the table
    content_width, value_width, _ = cli.get_widths(title)

    total_value = cli.items_sum()
    print()
    print(f"{title: ^{content_width+value_width + 5}}")
    print(cli.table_line())
    for debt in expense_debts:
        print(f"{debt.label: <{content_width}} R$ {debt.value: >{value_width}.2f}")
    print(cli.table_line())
    print(f"{'Total': <{content_width}} R$ {total_value: >{value_width}.2f}")
    print("\n")
