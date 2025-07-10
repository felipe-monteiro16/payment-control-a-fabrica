"""Get the information of contacts from a CSV file."""
import csv
from typing import List, Dict, Any
from data_classes import ExpenseDebt, Contact


def get_number_from_csv(user_id) -> List[Dict[str, Any]]:
    """Get the contact information for a given user_id from a CSV file."""
    user = Contact(name="", phone_number="")
    file_path = "data_access/src/contacts.csv"
    # Open the CSV file and read its contents
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("splitwise_id") == str(user_id):
                # Insert the user name and phone number into the dictionary
                user.name = row.get("name").strip()
                user.phone_number = row.get("phone_number").strip()
                break
    if not user.name or not user.phone_number:
        print(f"No contact found for user_id {user_id} in {file_path}")
    return user


def get_debts_from_csv(csv_path: str, user_id: str) -> tuple[list, float]:
    """Load CSV file and return a dictionary with user IDs and their debts."""
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        expenses: list[ExpenseDebt] = []
        for row in reader:
            if row["user_id"].strip() == user_id or row["user_id"].strip() == "":
                print("Skipping the current user from the CSV file.")
                continue
            try:
                user_id = str(row["user_id"].strip())
                amount = float(row["value"].strip().replace("R$", "").replace(",", "."))
            except ValueError:
                print(f"Failed to convert data: {row}")
                continue

            expenses.append(
                ExpenseDebt(id=user_id, label=row["name"].strip(), value=amount)
            )
        return expenses
