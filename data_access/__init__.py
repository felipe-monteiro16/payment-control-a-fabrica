"""Data Access Layer for Splitwise API"""
from .splitwise import get_all_users, get_user_debts
from .splitwise_config import config
from .csv_contacts import get_number_from_csv
from .splitwise import create_user_debts

class DataAccess:
    """Data Access Layer for Splitwise API"""
    def __init__(self):
        self.client, self.access_token = config()


    def get_all_users(self):
        """Get users from Splitwise API"""
        return get_all_users(self.client)


    def get_user_debts(self, user_id):
        """Get user debts from the last month by ID."""
        return get_user_debts(self.client, user_id)

    def get_user_contact(self, user_id):
        """Get user contact information from CSV file."""
        return get_number_from_csv(user_id)

    def create_user_debts(self, csv_path: str = None, description: str = None):
        """Send user debts to Splitwise API."""
        return create_user_debts(self.client, csv_path, description)
