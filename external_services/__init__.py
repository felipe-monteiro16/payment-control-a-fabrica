from .mercado_pago import get_payment_link, get_paid_debts
from .whatsapp_api import send_user

class ExternalServices:
    def __init__(self):
        self.services = {}

    def get_payment_link(self, user_debts, user_id) -> tuple[str, list[dict[str, float]]]:
        """Get the payment link for the given user_debts."""
        return get_payment_link(user_debts, user_id)


    def send_user(self, user_id: int, payment_link: str, payment_items: list[dict[str, float]]):
        """Send the payment link and items to the user."""
        send_user(user_id, payment_link, payment_items)


    def get_paid_debts(self):
        """Get the paid debts and remove then from json"""
        return get_paid_debts()
