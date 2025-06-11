"""Mercado Pago API integration for payment links."""
import os
import sys
import json
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import mercadopago


@dataclass
class Debt:
    """Class to represent user balance."""
    description: str
    value: float


    @property
    def full_description(self):
        """Get the description of the balance."""
        # Format the description with the value and date
        month_year = datetime.now().strftime("%m/%y")
        return self.description + month_year


@dataclass
class PaymentData:
    """Class to represent payment data."""
    tax_percent: float = 0.0099
    user_debts: list[Debt] = None
    # email: str = None


    def __init__(self, user_debts=None):
        if user_debts:
            self.user_debts = [
                Debt(debt["description"], float(debt["value"]))
                for debt in user_debts
            ]
        else:
            self.user_debts = []

        self.expiration_from = datetime.now(timezone.utc) # Today
        self.expiration_to = self.expiration_from + timedelta(days=20) # Today + Limit
        self.total_value = 0.0  # Initialize total_value in __init__
        self.json_filename = "payment_data.json"


    def has_debts(self):
        """Check if the user has debts."""
        return bool(self.user_debts)


    @property
    def settings(self):
        """Load Mercado Pago SDK settings."""
        load_dotenv()
        access_token = os.getenv("ACCESS_TOKEN")
        if not access_token:
            print("Mercado Pago ACCESS_TOKEN is missing. Please check your environment variables.")
            sys.exit("Please set the Mercado Pago ACCESS_TOKEN environment variable.")
        sdk = mercadopago.SDK(access_token)
        return sdk


    def get_taxes(self):
        """Calculate taxes for the given user debts."""
        # Calculate taxes
        debts_sum = sum(abs(debt.value) for debt in self.user_debts)
        taxes = round(debts_sum * self.tax_percent, 2)
        self.total_value = debts_sum + taxes
        self.user_debts.append(Debt("Taxas", taxes))


    @property
    def current_month(self) -> str:
        """Get the current month in the format 'MM/YY'."""
        return datetime.now().strftime("%m/%y").replace("/", "_")



    def to_json(self):
        """Convert user debts to JSON format."""
        return[
            {
                "title": debt.description,
                "quantity": 1,
                "unit_price": round(abs(debt.value), 2),
                "currency_id": "BRL"
            }
            for debt in self.user_debts
        ]


    def to_dict(self):
        """Convert user debts to a dictionary."""
        return[
            {
                "description": debt.description,
                "value": round(abs(debt.value), 2)
            }
            for debt in self.user_debts
        ]


    def to_payment_json(self, user_id, preference_data, payment_link):
        """Save the user debts to a json file"""
        payment_json = []

        if os.path.exists(self.json_filename):
            with open(self.json_filename, "r", encoding="utf-8") as json_file:
                try:
                    payment_json = json.load(json_file)
                except json.JSONDecodeError:
                    payment_json = []

        new_payment_entry = {
            "user_id": user_id,
            "external_reference": preference_data["external_reference"],
            "link": payment_link,
            "valor_total": self.total_value,
            "vencimento": preference_data["expiration_date_to"]
        }

        payment_json.append(new_payment_entry)

        # Salvar JSON em um arquivo
        with open("payment_data.json", "w", encoding="utf-8") as json_file:
            json.dump(payment_json, json_file, ensure_ascii=False, indent=4)


def get_payment_link(user_debts, user_id) -> tuple[str, list[Debt]]:
    """Get the payment link for the given user_id."""
    if user_debts is None:
        print("User debts cannot be None.")
        return None

    payment_data = PaymentData(user_debts)

    # Check if the user has debt
    if not payment_data.has_debts():
        print("User has no debts.")
        return None

    # Get the Mercado Pago SDK settings
    sdk = payment_data.settings
    payment_data.get_taxes()
    preference_items = payment_data.to_json()


    # Create preference data
    preference_data = {
        "items": preference_items,
        "payment_methods": {
            "excluded_payment_types": [
                {"id": "credit_card"},
                {"id": "debit_card"},
                {"id": "ticket"},  # boleto
                {"id": "balance"}
            ],
            "default_payment_method_id": "pix"
        },
        "description": "TESTE DE DESCRIÇÃO",
        "external_reference": f"{user_id}_{payment_data.current_month}",
        "expiration_date_from": payment_data.expiration_from.isoformat(),
        "expiration_date_to": payment_data.expiration_to.isoformat(),
    }

    # Create payment link
    payment_items = payment_data.to_dict()
    preference_response = sdk.preference().create(preference_data)
    if preference_response["status"] == 201:
        preference = preference_response["response"]
        payment_link = preference["init_point"]

        # Criar JSON consolidado com total
        payment_data.to_payment_json(user_id, preference_data, payment_link)
        return payment_link, payment_items

    # If the response is not 201, print the error and exit
    print(
        f"Error creating payment link: {preference_response['response']}."
        f"Status: {preference_response.get('status')}, "
        f"Error: {preference_response['response'].get('message', 'No message available')}"
    )
    sys.exit("Failed to create payment link.")


def get_paid_debts():
    """Get the paid debts with webhook"""
