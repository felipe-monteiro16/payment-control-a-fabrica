"""Get the information of contacts from a CSV file."""
import csv
from typing import List, Dict, Any


def get_number_from_csv(user_id) -> List[Dict[str, Any]]:
    """Get the contact information for a given user_id from a CSV file."""
    user = {}
    file_path = "data_access/src/contacts.csv"
    # Open the CSV file and read its contents
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("splitwise_id") == str(user_id):
                # Insert the user name and phone number into the dictionary
                user["name"] = row.get("name")
                user["phone_number"] = row.get("phone_number")
                break
    if not user:
        raise ValueError(f"No contact found for user_id {user_id} in {file_path}")
    return user
