"""Mercado Pago API integration for payment links."""
import os
import sys
from dataclasses import dataclass
from datetime import datetime
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
        self.user_debts.append(Debt("Taxas", taxes))


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


def get_payment_link(user_debts) -> tuple[str, list[Debt]]:
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
    }

    # Create payment link
    payment_items = payment_data.to_dict()
    preference_response = sdk.preference().create(preference_data)
    if preference_response["status"] == 201:
        preference = preference_response["response"]
        payment_link = preference["init_point"]
        return payment_link, payment_items

    # If the response is not 201, print the error and exit
    print(
        f"Error creating payment link: {preference_response['response']}."
        f"Status: {preference_response.get('status')}, "
        f"Error: {preference_response['response'].get('message', 'No message available')}"
    )
    sys.exit("Failed to create payment link.")
