import json
import os
from decimal import Decimal
from features.models.expense import Expense
from features.store.ports.expense_store import ExpenseStore


class JsonExpenseStore(ExpenseStore):
    def __init__(self, filepath: str = "expenses.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Creates an empty JSON array file if one doesn't exist yet."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def get_all(self) -> list[Expense]:
        """Reads the JSON file and reconstructs Expense objects."""
        with open(self.filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

        expenses = []
        for item in data:
            # Reconstruct the Expense object.
            expense = Expense(
                id=item.get("id"),
                description=item["description"],
                amount=Decimal(str(item["amount"])),
                date=item["date"],
            )
            expenses.append(expense)

        return expenses

    def save(self, expense: Expense) -> None:
        """Assigns an ID and saves the new expense to the file."""
        expenses = self.get_all()

        # 1. The Storage Manager computes the ID
        if not expenses:
            expense.id = 1
        else:
            # Find the highest existing ID and add 1
            highest_id = max(e.id for e in expenses if e.id is not None)
            expense.id = highest_id + 1

        # 2. Add to our list
        expenses.append(expense)

        # 3. Write everything back to disk
        self._save_all(expenses)

    def delete(self, expense_id: int) -> bool:
        """Removes an expense by ID and rewrites the file."""
        expenses = self.get_all()
        initial_count = len(expenses)

        # Keep everything EXCEPT the one with the matching ID
        filtered_expenses = [e for e in expenses if e.id != expense_id]

        if len(filtered_expenses) == initial_count:
            return False  # Nothing was deleted

        self._save_all(filtered_expenses)
        return True

    def _save_all(self, expenses: list[Expense]) -> None:
        """Helper method to serialize the objects back to JSON."""
        data = []
        for e in expenses:
            data.append(
                {
                    "id": e.id,
                    "description": e.description,
                    "amount": str(
                        e.amount
                    ),  # Convert Decimal to str for safe JSON storage
                    "date": e.date,
                }
            )

        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
