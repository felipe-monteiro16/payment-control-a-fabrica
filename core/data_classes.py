"""This module contains data classes used in the application"""
from dataclasses import dataclass
from datetime import datetime, timezone


def get_current_month() -> str:
    """Get the current month in the format 'MM/YY'."""
    return datetime.now(timezone.utc).strftime("%m/%y")


@dataclass
class ExpenseDebt:
    """Class to represent user debt from a Splitwise expense."""
    id: str # User ID
    label: str # User name
    value: float # User balance on the expense


@dataclass
class Debt:
    """Class to represent user debt in the Splitwise API."""
    label: str
    value: float

    @property
    def full_description(self) -> str:
        """Get the description of the debt."""
        # Format the description with the value and date
        return f"{self.label} - {get_current_month()}"


@dataclass
class Contact:
    """Class to represent a contact in the WhatsApp API."""
    name: str
    phone_number: str
