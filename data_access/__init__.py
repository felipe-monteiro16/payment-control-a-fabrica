"""Data Access Layer for Splitwise API"""
from .splitwise import get_all_users, get_user_debts
from .splitwise_config import config
from .mercado_pago import get_payment_link

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


    def get_payment_link(self, user_id):
        """Get the payment link for the given user_id."""
        return get_payment_link(self.client, user_id)
