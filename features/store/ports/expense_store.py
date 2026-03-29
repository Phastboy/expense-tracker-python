from abc import ABC, abstractmethod
from features.models.expense import Expense


class ExpenseStore(ABC):
    """
    This is an abstract class. It cannot be instantiated directly.
    Any class that inherits from this MUST implement these methods.
    """

    @abstractmethod
    def save(self, expense: Expense) -> None:
        """Saves a new expense and assigns it a unique ID."""
        pass

    @abstractmethod
    def get_all(self) -> list[Expense]:
        """Retrieves all saved expenses."""
        pass

    @abstractmethod
    def delete(self, expense_id: int) -> bool:
        """Deletes an expense by its ID. Returns True if successful."""
        pass
