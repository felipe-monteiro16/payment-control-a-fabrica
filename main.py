"""Splitwise API Python Client"""
from data_access import DataAccess


def main():
    """Main function to run the Splitwise API client."""
    # Initialize the Data Access Layer
    data_access = DataAccess()

    # Get users from Splitwise API
    users = data_access.get_all_users()
    for user in users:
        print(f"User ID: {user['id']}, Name: {user['first_name']} {user['last_name']}")


if __name__ == "__main__":
    main()
