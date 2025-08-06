"""
Manages application logs for the monthly expense tracking system.

This module handles the storage of various application events (e.g., WhatsApp messages,
payment link creations, Splitwise entries) into separate JSON files within the 'logs/' directory.
It ensures safe append operations and consistent data fo0rmatting.
"""
import os
import json
from core import Contact

# Define the log directory paths
PAYMENT_LINK_LOG_PATH = "logs/payment_links.json" # Mercado Pago Payment Links
EXPENSES_LOG_PATH = "logs/expenses.json"          # Splitwise Entries
WHATSAPP_LOG_PATH = "logs/whatsapp_messages.json" # WhatsApp Messages

class Logger:
    """Logger class to handle logging of various application events."""

    def __init__(self):
        """Initialize the Logger and ensure log directories exist."""
        os.makedirs("logs", exist_ok=True)
        self._initialize_log_files()

    def _initialize_log_files(self):
        """Create log files if they do not exist."""
        for path in [PAYMENT_LINK_LOG_PATH, EXPENSES_LOG_PATH, WHATSAPP_LOG_PATH]:
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump([], f)


    @staticmethod
    def _append_to_log(log_path: str, log_entry: dict) -> None:
        """Append a log entry to the specified log file."""
        # Verify if the folder exists, if not create it
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Verify if the log file exists and append the entry
        if not os.path.exists(log_path):
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump([], f)  # Create an empty list if file does not exist

        # Append the log entry
        with open(log_path, 'r+', encoding='utf-8') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            f.truncate()  # Clear the file content
            json.dump(logs, f, indent=4, ensure_ascii=False)


    @staticmethod
    def log_payment_link(user_id, external_ref, payment_link: str, total_value, expiration) -> None:
        """Log the creation of a payment link for a user."""
        log_entry = {
            "user_id": user_id,
            "external_ref": external_ref,
            "payment_link": payment_link,
            "total_value": total_value,
            "expiration": expiration
        }
        Logger._append_to_log(PAYMENT_LINK_LOG_PATH, log_entry)


    @staticmethod
    def log_whatsapp_message(
        contact: Contact, parameters: dict, payment_link: str
    ) -> None:
        """Log the sending of a WhatsApp message."""
        log_entry = {
            "contact": {
                "name": contact.name,
                "phone_number": contact.phone_number
            },
            "parameters": parameters,
            "payment_link": payment_link
        }
        Logger._append_to_log(WHATSAPP_LOG_PATH, log_entry)
