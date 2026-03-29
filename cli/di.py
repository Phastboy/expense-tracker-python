from features.store.adapters.json_expense_store import JsonExpenseStore
from features.use_cases.add_expense import AddExpenseUseCase
from features.use_cases.list_expenses import ListExpensesUseCase
from features.use_cases.delete_expense import DeleteExpenseUseCase

store = JsonExpenseStore("expenses.json")

add_expense_use_case = AddExpenseUseCase(store)
list_expenses_use_case = ListExpensesUseCase(store)
delete_expense_use_case = DeleteExpenseUseCase(store)
