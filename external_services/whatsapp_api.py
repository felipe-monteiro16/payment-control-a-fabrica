"""Module to send messages via WhatsApp API."""
import os
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
import requests
from data_access import DataAccess


@dataclass
class Debt:
    """Class to represent user balance."""
    description: str
    value: float


    @property
    def full_description(self):
        """Get the description of the balance."""
        # Format the description with the value and date
        month_year = MessageData().current_month()
        return f"{self.description.capitalize()} {month_year}"



class MessageData:
    """Proccess the data for sending messages via WhatsApp API."""
    payment_items: list[Debt] = None

    def __init__(self, payment_items: list[dict[str, float]] = None):
        if payment_items:
            self.payment_items = [
                Debt(debt["description"], float(debt["value"]))
                for debt in payment_items
            ]
        else:
            self.payment_items = []

    def env(self):
        """Load environment variables for WhatsApp API credentials."""
        load_dotenv()
        phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        if not phone_number_id or not access_token:
            raise ValueError("WhatsApp API credentials are not set in the environment variables.")
        return phone_number_id, access_token

    def get_user_contact(self, user_id: int) -> dict[str, str]:
        """Get the user's contact information from the CSV file."""
        data_access = DataAccess()
        user_contact = data_access.get_user_contact(user_id)
        return user_contact


    @property
    def current_month(self) -> str:
        """Get the current month in the format 'MM/YY'."""
        return datetime.now().strftime("%m/%y")

    def get_total_value(self) -> float:
        """Calculate the total value of the payment items."""
        self.payment_items.append(Debt("Total", sum(item.value for item in self.payment_items)))


    def align_payment_values(self) -> None:
        """Align the payment values"""
        for item in self.payment_items:
            item.value = f"{item.value:.2f}".replace(".", ",")


        def get_spaces(value: str) -> str:
            """Get the number of spaces needed to align the values."""
            return " " * (7 - len(value))


        for item in self.payment_items:
            item.value = f"{get_spaces(item.value)}{item.value}"


    @property
    def to_whatsapp_payload(self):
        """Convert the payment items to a format suitable for WhatsApp API."""
        self.get_total_value()
        self.align_payment_values()
        parameters = {}
        for item in self.payment_items:
            description = item.description.split()[0].lower()
            parameters[description] = item.value
        return parameters


def send_user(user_id: int, payment_link: str, payment_items: list[dict[str, float]]) -> None:
    """Send the payment link and items to the user via WhatsApp API."""

    message_data = MessageData(payment_items)
    phone_number_id, access_token = message_data.env()
    user_contact = message_data.get_user_contact(user_id)
    current_month = message_data.current_month
    items = message_data.to_whatsapp_payload
    payment_link = payment_link.split("pref_id=")[1]

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": user_contact["phone_number"],
        "type": "template",
        "template": {
            "name": "resumo_mensal_a_fabrica",
            "language": { "code": "pt_BR" },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": user_contact["name"]},
                        {"type": "text", "text": current_month},
                        {"type": "text", "text": items["mensalidade"]},
                        {"type": "text", "text": items["almoço"]},
                        {"type": "text", "text": items["geladeira"]},
                        {"type": "text", "text": items["taxas"]},
                        {"type": "text", "text": items["total"]}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": 0,
                    "parameters": [
                        {"type": "text", "text": payment_link}
                    ]
                }
            ]
        }
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(response.status_code)
    print(response.json())
