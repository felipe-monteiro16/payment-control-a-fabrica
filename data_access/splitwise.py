"""Data Access Layer for Splitwise API"""
import csv
from splitwise.expense import Expense
from splitwise.user import ExpenseUser


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

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                user_id = int(row["UserID"].strip())
                amount = float(row["Valor"].strip().replace("R$", "").replace(",", "."))
            except ValueError:
                print(f"Failed to convert data: {row}")
                continue

            total_amount += amount

            user = ExpenseUser()
            user.setId(user_id)
            user.setPaidShare("0.00")         # A pessoa não pagou nada
            user.setOwedShare(str(amount))    # Mas está devendo esse valor
            participants.append(user)

    if not participants:
        print("No valid participants found. Aborting.")
        return

    #  Adds the current user as the payer
    pagador = ExpenseUser()
    pagador.setId(client.getCurrentUser().id)
    pagador.setPaidShare(str(total_amount))
    pagador.setOwedShare("0.00")
    participants.append(pagador)

    expense = Expense()
    expense.setCost(str(total_amount))
    expense.setDescription(description)
    expense.setUsers(participants)

    created_expense, errors = client.createExpense(expense)

    if created_expense and created_expense.getId():
        print(f"Expense created successfully! ID: {created_expense.getId()}")
    else:
        print("Failed to create expense.")
        if errors:
            print("Errors:", errors)
        else:
            print("No specific error was returned.")
