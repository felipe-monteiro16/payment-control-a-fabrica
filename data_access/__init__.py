"""Data Access Layer for Splitwise API"""
from .splitwise import get_all_users
from .splitwise_config import config


class DataAccess:
    """Data Access Layer for Splitwise API"""
    def __init__(self):
        self.client, self.access_token = config()


    def get_all_users(self):
        """Get users from Splitwise API"""
        return get_all_users(self.client)
