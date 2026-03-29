from features.store.adapters.json_expense_store import JsonExpenseStore
from features.use_cases.add_expense import AddExpenseUseCase
from features.use_cases.list_expenses import ListExpensesUseCase
from features.use_cases.delete_expense import DeleteExpenseUseCase
from typing import Optional

_store: Optional[JsonExpenseStore] = None


def get_store(filepath: str = "expenses.json") -> JsonExpenseStore:
    """Lazy-initialize and return the expense store."""
    global _store
    if _store is None:
        _store = JsonExpenseStore(filepath)
    return _store


def get_add_expense_use_case() -> AddExpenseUseCase:
    """Lazy-initialize and return the add expense use case."""
    return AddExpenseUseCase(get_store())


def get_list_expenses_use_case() -> ListExpensesUseCase:
    """Lazy-initialize and return the list expenses use case."""
    return ListExpensesUseCase(get_store())


def get_delete_expense_use_case() -> DeleteExpenseUseCase:
    """Lazy-initialize and return the delete expense use case."""
    return DeleteExpenseUseCase(get_store())
