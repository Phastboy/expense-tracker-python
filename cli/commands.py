import typer
from decimal import Decimal
from cli import di
from cli import views

app = typer.Typer(help="A beautiful, mathematically accurate expense tracker.")


@app.command()
def add(description: str, amount: str):
    """Adds a new expense to your tracker."""
    try:
        decimal_amount = Decimal(amount)

        expense = di.add_expense_use_case.execute(description, decimal_amount)

        views.display_success(f"Added: {expense.description} for ${expense.amount:.2f}")
    except ValueError as e:
        views.display_error(str(e))


@app.command()
def ls():
    """Lists all recorded expenses."""
    expenses = di.list_expenses_use_case.execute()

    views.display_expenses_table(expenses)


@app.command()
def delete(expense_id: int):
    """Deletes an expense by its ID."""
    try:
        di.delete_expense_use_case.execute(expense_id)

        views.display_success(f"Successfully deleted expense #{expense_id}")
    except ValueError as e:
        views.display_error(str(e))
