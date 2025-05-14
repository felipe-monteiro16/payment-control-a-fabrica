"""Mercado Pago API integration for payment links."""
import os
import sys
from dotenv import load_dotenv
import mercadopago
from .splitwise import get_user_debts


# Load environment variables from .env file
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
sdk = mercadopago.SDK(ACCESS_TOKEN)
request_options = mercadopago.config.RequestOptions()


def get_payment_link(client, user_id: int):
    """Get the payment link for the given user_id."""

    # Get user debts from Splitwise API
    user_debts = get_user_debts(client, user_id)
    if not user_debts:
        print("No debts found for the user.")
        sys.exit(1)

    # Calculate taxes
    taxe_percent: float = 0.0099
    debts_sum = sum((debt["balance"] * -1) for debt in user_debts)
    taxes = round(debts_sum * taxe_percent, 2)

    # Create preference data
    preference_data = {
        "items": [
            {
            "title": "Taxas",
            "quantity": 1,
            "unit_price": taxes,
            "currency_id": "BRL"
            }
        ],
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

    # Add items to the preference data
    for debt in user_debts:
        preference_data["items"].insert(0,# Insert at the beginning
            {
                "title": debt["name"],
                "quantity": 1,
                "unit_price": round((debt["balance"] * -1), 2),
                "currency_id": "BRL"
            }
        )

    # Create payment link
    preference_response = sdk.preference().create(preference_data)
    if preference_response["status"] == 201:
        preference = preference_response["response"]
        payment_link = preference["init_point"]

        # Create items list to show in the response
        payment_items = [
            {
                "description": item["title"],
                "value": item["quantity"] * item["unit_price"]
            }
            for item in preference_data["items"]
        ]
        return payment_link, payment_items

    # If the response is not 201, print the error and exit
    print("Erro ao criar link de pagamento:", preference_response)
    sys.exit(1)
