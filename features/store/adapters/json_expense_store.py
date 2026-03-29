import json
import os
from decimal import Decimal, InvalidOperation
from typing import List, Optional, Dict, Any
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

    def _parse_expense(self, item: Dict[str, Any]) -> Optional[Expense]:
        """Safely parse a single expense from JSON data."""
        try:
            # Validate required fields
            if "description" not in item or "amount" not in item or "date" not in item:
                return None

            # Parse amount
            try:
                amount = Decimal(str(item["amount"]))
            except InvalidOperation, ValueError, TypeError:
                return None

            # Get ID (allow None for new records)
            expense_id = item.get("id")
            if expense_id is not None and not isinstance(expense_id, int):
                return None

            # Create expense with validation
            expense = Expense(
                id=expense_id,
                description=str(item["description"]),
                amount=amount,
                date=str(item["date"]),
            )
            return expense
        except ValueError, InvalidOperation:
            # Skip corrupted records
            return None

    def get_all(self) -> List[Expense]:
        """Reads the JSON file and reconstructs Expense objects."""
        try:
            with open(self.filepath, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    # Corrupted JSON file, return empty list
                    return []

            # Validate top-level structure
            if not isinstance(data, list):
                return []

            # Parse each expense, skipping corrupted ones
            expenses = []
            for item in data:
                if isinstance(item, dict):
                    expense = self._parse_expense(item)
                    if expense is not None:
                        expenses.append(expense)

            return expenses
        except IOError, OSError:
            # File system errors
            return []

    def _get_next_id(self, expenses: List[Expense]) -> int:
        """Calculate the next available ID safely."""
        ids = [e.id for e in expenses if e.id is not None]
        return max(ids) + 1 if ids else 1

    def save(self, expense: Expense) -> None:
        """Assigns an ID and saves the new expense to the file."""
        expenses = self.get_all()

        # Assign ID
        expense.id = self._get_next_id(expenses)

        # Add to list
        expenses.append(expense)

        # Write everything back to disk
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

    def _save_all(self, expenses: List[Expense]) -> None:
        """Helper method to serialize the objects back to JSON."""
        data = []
        for e in expenses:
            data.append(
                {
                    "id": e.id,
                    "description": e.description,
                    "amount": str(e.amount),
                    "date": e.date,
                }
            )

        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
