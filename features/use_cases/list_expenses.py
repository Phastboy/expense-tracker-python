from features.models.expense import Expense
from features.store.ports.expense_store import ExpenseStore


class ListExpensesUseCase:
    def __init__(self, store: ExpenseStore):
        self.store = store

    def execute(self) -> list[Expense]:
        """
        Retrieves all expenses from the store.
        """
        return self.store.get_all()
