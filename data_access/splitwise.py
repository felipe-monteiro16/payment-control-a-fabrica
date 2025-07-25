"""Data Access Layer for Splitwise API"""
from datetime import datetime, timedelta
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from core import Debt, ExpenseDebt, ExpenseType


class DebtProcessor:
    """Class to process user debts."""
    def __init__(self, client = None, csv_path: str = None):
        """Initialize the DebtProcessor with a Splitwise client and CSV path."""
        self.csv_path = csv_path if csv_path else None
        self.user_id = client.getCurrentUser().id if client else None


    def to_dict(self, expenses: list[ExpenseDebt]) -> list[dict[str, str]]:
        """Convert a list of Debt objects to a list of dictionaries."""
        return [
            {
                "user_id": expense.id,
                "name": expense.label,
                "value": expense.value,
            }
            for expense in expenses
        ]


    def get_total_amount(self, expenses: list[ExpenseDebt]) -> float:
        """Get the total amount from a list of Debt objects."""
        return sum(float(expense.value) for expense in expenses)


    def verify_friend_balances(self, friend_balances: list[Debt]) -> bool:
        """Verify if the friend balances match the expected expense types."""
        if not friend_balances:
            return False

        # Get a list of expense types
        expense_types = [expense.value.lower() for expense in ExpenseType]

        # Check if each friend balance matches with an expense type
        for balance in friend_balances:
            balance.label = balance.label.split()[0].lower()  # Normalize the label to lowercase
            for i, expense_type in enumerate(expense_types):
                if expense_type == balance.label:
                    # Remove the matched type to ensure one of each type is used
                    del expense_types[i]
                    break

        if len(expense_types) == 0:
            # All balances matched the expected expense types
            return True

        # If we reach here, a balance did not match any expense type
        print("Not all balances matched the expected expense types.")
        return False


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


def get_user_debts(client, friend_id) -> list[Debt]:
    """Get user debts from the last 30 days by ID."""
    friend_balances = []
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)

    # Get the expenses from the last 30 days
    expenses = client.getExpenses(dated_after=thirty_days_ago.strftime("%Y-%m-%d"), limit=100)

    # Get the friend debts
    for expense in expenses:
        if expense.payment:  # Skip payment expenses
            continue
        len_friend_balances = len(friend_balances)

        # Find the debts for the specified friend
        for user in expense.getUsers():
            if user.id == friend_id:
                balance = user.getNetBalance()
                if balance:  # Only append if there is a valid balance
                    friend_balances.append(
                        Debt(label=expense.description, value=abs(float(balance)))
                    )
                    break

        # If the friend isn't in the expense, we append a zero balance
        if len_friend_balances == len(friend_balances):
            friend_balances.append(
                Debt(label=expense.description, value=0.00)
            )

        # Stop after len(ExpenseType) valid expenses
        if len(friend_balances) == len(ExpenseType):
            # Verify if the friend balances match the expected expense types
            debt_processor = DebtProcessor()
            if debt_processor.verify_friend_balances(friend_balances):
                return friend_balances

    # If we reach here, it means we didn't find enough expenses for the friend
    return None


def create_user_debts(client, csv_path, description, expenses) -> tuple[list[dict], str]:
    """Create a new expense based on a CSV file with user debts."""

    participants = []
    total_amount = 0
    user_id = client.getCurrentUser().id
    debt_processor = DebtProcessor(client, csv_path)
    total_amount = debt_processor.get_total_amount(expenses)

    if total_amount <= 0:
        print("Total amount is zero or negative. Aborting.")
        return
    if not expenses:
        print("No expenses found in the CSV file. Aborting.")
        return

    for expense in expenses:
        # Creates an ExpenseUser object for each participant
        user = ExpenseUser()
        user.setId(expense.id)
        user.setPaidShare("0.00")
        user.setOwedShare(expense.value)
        participants.append(user)

    if not participants:
        print("No valid participants found. Aborting.")
        return

    # Adds the current user as the payer
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
        return expenses, description
    print("Failed to create expense.")
    if errors:
        print("Errors:", errors)
    else:
        print("No specific error was returned.")
    return [], description


def send_payments(client, paid_users: list[int]):
    """Send payments of the paid users to the Splitwise API."""
    if len(paid_users) == 0 or not paid_users:
        print("No paid users found. Aborting.")
        return

    friends = client.getFriends()

    for user_id in paid_users:
        # Find the user in the friends list
        user = None
        for friend in friends:
            if str(friend.id) == str(user_id):
                user = friend
                break
        if not user:
            print(f"User with ID {user_id} not found.")
            continue

        # Get the user's balance
        user_balance = None
        for balance in user.getBalances():
            if balance.getCurrencyCode() == "BRL":
                try:
                    user_balance = balance.getAmount()
                except UnboundLocalError as e:
                    print(f"Error getting balance for user {user.first_name}. ID {user_id}: {e}")
                break

        # If the user has no balance or is already paid off, skip
        if user_balance is None or float(user_balance) <= 0:
            print(f"The user is already paid off. Name {user.first_name}. ID {user_id}.")
            continue

        # Creating payment
        payment = Expense()
        payment.setCost(str(user_balance))
        payment.setDescription("Pagamento do Mês")
        payment.setPayment(True)

        # Friend
        payer = ExpenseUser()
        payer.setId(user_id)
        payer.setPaidShare(str(user_balance))
        payer.setOwedShare("0.00")

        # Current user
        recipient = ExpenseUser()
        recipient.setId(client.getCurrentUser().id)
        recipient.setPaidShare("0.00")
        recipient.setOwedShare(str(user_balance))

        # Create the payment with both users
        payment.setUsers([payer, recipient])
        payment.setCurrencyCode("BRL")
        created_payment, errors = client.createExpense(payment)

        # Check if the payment was created successfully
        if created_payment and created_payment.getId():
            print(f"Payment sent for user {user.first_name}. ID {user_id}. Balance: {user_balance}")
        else:
            print(f"Failed to send payment for user {user.first_name}. ID {user_id}.")
            if errors:
                print("Errors:", errors)
            else:
                print("No specific error was returned.")
        print()
