"""Module containing enum classes for the application."""
from enum import Enum


class ExpenseType(Enum):
    """Class to represent different types of expenses."""
    MENSALIDADE = "Mensalidade"
    ALMOCO = "Almoço"
    GELADEIRA = "Geladeira"
