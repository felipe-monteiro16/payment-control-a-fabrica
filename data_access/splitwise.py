"""Data Access Layer for Splitwise API"""
import csv
from dataclasses import dataclass
from splitwise.expense import Expense
from splitwise.user import ExpenseUser


@dataclass
class Debt:
    """Class to represent user balance."""
    id: str
    name: str
    value: str


@dataclass
class DebtProcessor:
    """Class to process user debts."""
    def __init__(self, client, csv_path: str = "data_access/src/debts.csv"):

        self.csv_path = csv_path
        self.user_id = client.getCurrentUser().id


    def load_csv(self) -> tuple[list, float]:
        """Load CSV file and return a dictionary with user IDs and their debts."""
        with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            expenses: list[Debt] = []
            total_amount = 0.0
            for row in reader:
                if row["UserID"].strip() == self.user_id or row["UserID"].strip() == "":
                    print("Skipping the current user from the CSV file.")
                    continue
                try:
                    user_id = str(row["user_id"].strip())
                    amount = float(row["value"].strip().replace("R$", "").replace(",", "."))
                except ValueError:
                    print(f"Failed to convert data: {row}")
                    continue

                total_amount += amount
                expenses.append(
                    Debt(id=user_id, name=row["name"].strip(), value=str(amount))
                )
            return expenses, total_amount


    def to_dict(self, expenses: list[Debt]) -> list[dict]:
        """Convert a list of Debt objects to a list of dictionaries."""
        return [
            {
                "user_id": expense.id,
                "name": expense.name,
                "value": expense.value,
            }
            for expense in expenses
        ]


def get_all_users(client):
    """Get all users from Splitwise API"""
    users = []
    friends = client.getFriends()
    for friend in friends:
        friend.id = friend.id or "Unknown"
        friend.first_name = friend.first_name or "Unknown"
        friend.last_name = friend.last_name or "Unknown"
        users.append(
            {
                "id": friend.id,
                "first_name": friend.first_name,
                "last_name": friend.last_name,
            }
        )
    return users


def get_user_debts(client, friend_id) -> list[dict[str, float]]:
    """Get user debts from the last month by ID."""
    valid_expenses_cont = 0
    friend_balances = []
    expenses = client.getExpenses(offset=0, limit=50) # What is the limit?
    for expense in expenses:
        if expense.payment: # Skip payment expenses
            continue
        valid_expenses_cont += 1
        len_friend_balances = len(friend_balances)
        for user in expense.getUsers():
            if user.id == friend_id:
                balance = user.getNetBalance()
                if balance: # Only append if there is a valid balance
                    friend_balances.append(
                        {'description': expense.description, 'value': abs(float(balance))}
                    )
                    break
        # If the friend aren't in the expense, we append a zero balance
        if len_friend_balances == len(friend_balances):
            friend_balances.append(
                {'description': expense.description, 'value': 0.00}
            )

        # Stop after 3 valid expenses
        if valid_expenses_cont == 3:

            return friend_balances

    # If we reach here, it means we didn't find 3 expenses for the friend
    if friend_balances:
        return friend_balances
        # return UserBalances(friend_balances)
    return None


def create_user_debts(client, csv_path="data_access/src/debts.csv", description="New Expense"):
    """Create a new expense based on a CSV file with user debts."""

    participants = []
    total_amount = 0
    user_id = client.getCurrentUser().id

    debt_processor = DebtProcessor(client, csv_path)
    expenses, total_amount = debt_processor.load_csv()
    if total_amount <= 0:
        print("Total amount is zero or negative. Aborting.")
        return
    if not expenses:
        print("No expenses found in the CSV file. Aborting.")
        return

    for expense in expenses:
        user = ExpenseUser()
        user.setId(expense.id)  # Use the user ID from the expense
        user.setPaidShare("0.00")         # A pessoa não pagou nada
        user.setOwedShare(expense.value)    # Mas está devendo esse valor
        participants.append(user)

    if not participants:
        print("No valid participants found. Aborting.")
        return

    #  Adds the current user as the payer
    payer = ExpenseUser()
    payer.setId(user_id)
    payer.setPaidShare(str(total_amount))
    payer.setOwedShare("0.00")
    participants.append(payer)

    expense = Expense()
    expense.setCost(str(total_amount))
    expense.setDescription(description)
    expense.setUsers(participants)

    created_expense, errors = client.createExpense(expense)

    if created_expense and created_expense.getId():
        print(f"Expense created successfully! ID: {created_expense.getId()}")
        return debt_processor.to_dict(expenses), description
    print("Failed to create expense.")
    if errors:
        print("Errors:", errors)
    else:
        print("No specific error was returned.")
