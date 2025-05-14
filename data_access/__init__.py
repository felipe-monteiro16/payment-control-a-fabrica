"""Data Access Layer for Splitwise API"""
from .splitwise import get_all_users, get_user_debts
from .splitwise_config import config


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
