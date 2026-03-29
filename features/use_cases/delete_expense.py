from features.store.ports.expense_store import ExpenseStore


class DeleteExpenseUseCase:
    def __init__(self, store: ExpenseStore):
        self.store = store

    def execute(self, expense_id: int) -> bool:
        """
        Validates the ID and deletes the expense.
        """
        if expense_id <= 0:
            raise ValueError("Expense ID must be a positive integer.")

        success = self.store.delete(expense_id)

        if not success:
            raise ValueError(f"Expense with ID {expense_id} not found.")

        return True
