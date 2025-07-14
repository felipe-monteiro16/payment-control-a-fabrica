"""Module to send messages via WhatsApp API."""
import os
import sys
from dotenv import load_dotenv
import requests
from core import Debt, Contact, get_current_month


class MessageData:
    """Process the data for sending messages via WhatsApp API."""
    payment_items: list[Debt] = None

    def __init__(self, payment_items: list[dict[str, float]] = None):
        if payment_items:
            self.payment_items = [
                Debt(debt.label, float(debt.value))  # Ensure value is a float
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


    def get_total_value(self) -> float:
        """Calculate the total value of the payment items."""
        self.payment_items.append(Debt("Total", sum(item.value for item in self.payment_items)))


    def align_payment_values(self) -> None:
        """Align the payment values"""
        for item in self.payment_items:
            item.value = f"{item.value:.2f}".replace(".", ",")


        def get_spaces(value: str) -> str:
            """Get the number of spaces needed to align the values."""
            return " " * (len("0000,00") - len(value))


        for item in self.payment_items:
            item.value = f"{get_spaces(item.value)}{item.value}"


    def to_whatsapp_payload(self):
        """Convert the payment items to a format suitable for WhatsApp API."""
        self.get_total_value()
        self.align_payment_values()
        parameters = {}
        for item in self.payment_items:
            label = item.label.split()[0].lower()
            parameters[label] = item.value
        return parameters


    def get_debt_value(self, label: str) -> str:
        """Get the value of a specific debt item."""
        for item in self.payment_items:
            if item.label.lower().split()[0] == label.lower():
                return item.value
        return "   0,00"


def send_debt_to_user(
    user_contact: Contact,
    payment_link: str,
    payment_items: list[Debt] = None
) -> None:
    """Send the payment link and items to the user via WhatsApp API."""
    if not user_contact or not payment_link or not payment_items:
        print("User contact, payment link, and payment items must be provided.")
        return

    message_data = MessageData(payment_items)
    phone_number_id, access_token = message_data.env()
    current_month = get_current_month()
    message_data.to_whatsapp_payload()

    content_link = ""
    if "pref_id=" in payment_link:
        content_link = payment_link.split("pref_id=", 1)[1]
    else:
        raise ValueError("The payment_link does not contain 'pref_id='.")

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": user_contact.phone_number,
        "type": "template",
        "template": {
            "name": "cobranca_mensal_a_fabrica",
            "language": { "code": "pt_BR" },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": user_contact.name},
                        {"type": "text", "text": current_month},
                        {"type": "text", "text": message_data.get_debt_value("mensalidade")},
                        {"type": "text", "text": message_data.get_debt_value("almoço")},
                        {"type": "text", "text": message_data.get_debt_value("geladeira")},
                        {"type": "text", "text": message_data.get_debt_value("taxas")},
                        {"type": "text", "text": message_data.get_debt_value("total")}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": 0,
                    "parameters": [
                        {"type": "text", "text": content_link}
                    ]
                }
            ]
        }
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"Message sent successfully to {user_contact.name}.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, "
              f"Response: {response.text}")
        print(f"WhatsApp API error: {response.status_code} - {response.text}")
        sys.exit(1)
