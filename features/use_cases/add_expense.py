from decimal import Decimal
from features.models.expense import Expense
from features.store.ports.expense_store import ExpenseStore


class AddExpenseUseCase:
    def __init__(self, store: ExpenseStore):
        """
        We inject the abstract ExpenseStore.
        This use case doesn't know (or care) if it's saving to JSON or SQL.
        """
        self.store = store

    def execute(self, description: str, amount: Decimal) -> Expense:
        """
        Validates input, creates the expense, and saves it.
        """
        if not description or not description.strip():
            raise ValueError("Expense description cannot be empty.")

        if amount <= 0:
            raise ValueError("Expense amount must be greater than zero.")

        expense = Expense(description=description.strip(), amount=amount)

        self.store.save(expense)

        return expense
