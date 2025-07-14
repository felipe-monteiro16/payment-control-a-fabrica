"""Data Access Layer for Splitwise API"""
from config.splitwise_config import config
from .splitwise import get_all_users, get_user_debts, create_user_debts, send_payments
from .csv_manager import get_number_from_csv, get_debts_from_csv

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


    def get_debts_from_csv(self, user_id: str = None, csv_path: str = None) -> tuple[list, float]:
        """Get user debts from the CSV file."""
        if not csv_path:
            csv_path = "data_access/src/debts.csv"
        return get_debts_from_csv(csv_path, user_id)


    def create_user_debts(self, csv_path, description, expenses: list = None):
        """Send user debts to Splitwise API."""
        return create_user_debts(self.client, csv_path, description, expenses)


    def send_payments(self, paid_users: list[int]):
        """Send payments to the Splitwise API."""
        return send_payments(self.client, paid_users)
