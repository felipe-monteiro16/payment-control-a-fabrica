"""Data Access Layer for Splitwise API"""


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
