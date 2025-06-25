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
        return f"{self.description} - {month_year}"


@dataclass
class PaymentData:
    """Class to represent payment data."""
    tax_percent: float = 0.0099
    user_debts: list[Debt] = None
    # email: str = None
    expiration_from: datetime = None
    expiration_to: datetime = None


    def __init__(self):
        self.total_value = 0.0  # Initialize total_value in __init__
        self.json_filename = "payment_data.json"


    @property
    def settings(self):
        """Load Mercado Pago SDK settings."""
        load_dotenv()
        access_token = os.getenv("ACCESS_TOKEN")
        if not access_token:
            print("Mercado Pago ACCESS_TOKEN is missing. Please check your environment variables. "
                  "You can set it by adding 'ACCESS_TOKEN=<your_token>' to your .env file.")
        sdk = mercadopago.SDK(access_token)
        return sdk


    def get_debts(self, user_debts=None):
        """Get the debts with Debt type"""
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


    def get_taxes(self):
        """Calculate taxes for the given user debts."""
        # Calculate taxes
        debts_sum = sum(abs(debt.value) for debt in self.user_debts)
        taxes = round(debts_sum * self.tax_percent, 2)
        self.total_value = debts_sum + taxes
        self.user_debts.append(Debt("Taxas", taxes))


    def set_expiration(self):
        """Set the expiration to the payment_link"""
        self.expiration_from = datetime.now(timezone.utc) # Today
        self.expiration_to = self.expiration_from + timedelta(days=20) # Today + Limit


    @property
    def current_month(self) -> str:
        """Get the current month in the format 'MM/YY'."""
        return datetime.now().strftime("%m_%y")


    def external_reference(self, user_id):
        """Set external reference to the payment"""
        version = 1
        external_reference = f"{user_id}_{self.current_month}_V{version}"

        # Get correct version
        with open("payment_data.json", "r", encoding="utf-8") as json_file:
            try:
                payment_data = json.load(json_file)
                for entry in payment_data:
                    if entry.get("external_reference") == external_reference:
                        version+=1
                        external_reference = f"{user_id}_{self.current_month}_V{version}"
            except json.JSONDecodeError:
                print("Error decoding payment data.")
                return []
        return external_reference


    def to_json(self):
        """Convert user debts to JSON format for preference data."""
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

        # Save JSON to a file
        with open("payment_data.json", "w", encoding="utf-8") as json_file:
            json.dump(payment_json, json_file, ensure_ascii=False, indent=4)


def create_payment_link(user_debts, user_id) -> tuple[str, list[Debt]]:
    """Get the payment link for the given user_id."""
    if user_debts is None:
        print("User debts cannot be None.")
        return None

    payment_data = PaymentData()
    payment_data.get_debts(user_debts)

    # Check if the user has debt
    if not payment_data.has_debts():
        print("User has no debts.")
        return None

    # Get the Mercado Pago SDK settings
    sdk = payment_data.settings
    payment_data.get_taxes()
    payment_data.set_expiration()
    preference_items = payment_data.to_json()
    external_reference = payment_data.external_reference(user_id)

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
        "external_reference": f"{external_reference}",
        "expiration_date_from": payment_data.expiration_from.isoformat(),
        "expiration_date_to": payment_data.expiration_to.isoformat(),
    }

    # Create payment link
    payment_items = payment_data.to_dict()
    try:
        preference_response = sdk.preference().create(preference_data)
        if preference_response["status"] == 201:
            preference = preference_response["response"]
            payment_link = preference["init_point"]

            # Create consolidated JSON with total
            payment_data.to_payment_json(user_id, preference_data, payment_link)
            return payment_link, payment_items

        # If the response is not 201, print the error and exit
        print(
            f"Error creating payment link: {preference_response['response']}."
            f"Status: {preference_response.get('status')}, "
            f"Error: {preference_response['response'].get('message', 'No message available')}"
        )
    except KeyError as e:
        print(f"An error occurred while creating the payment link: {e}")
        sys.exit("Failed to create payment link.")


def get_paid_debts() -> list[int]:
    """Verify the debts, remove from json and return the paid."""
    # Initialize the PaymentData instance
    payment_data = PaymentData()
    sdk = payment_data.settings

    # Search for all payments
    search_result = sdk.payment().search({})

    # Filter the payments
    filtered_payments = [
        payment["external_reference"]
        for payment in search_result["response"]["results"]
        if (
            datetime.fromisoformat(payment["date_created"]).month == datetime.now().month and
            datetime.fromisoformat(payment["date_created"]).year == datetime.now().year and
            payment["status"] == "approved" and
            payment["external_reference"] is not None
        )
    ]

    # Extract user IDs from the approved payments
    user_ids = [int(ref.split("_")[0]) for ref in filtered_payments]

    return user_ids
