import typer
from decimal import Decimal, InvalidOperation
from cli import di
from cli import views

app = typer.Typer(help="A beautiful, mathematically accurate expense tracker.")


@app.command()
def add(description: str, amount: str):
    """Adds a new expense to your tracker."""
    try:
        # Parse amount with Decimal for precision
        try:
            decimal_amount = Decimal(amount)
        except InvalidOperation:
            views.display_error(
                f"Invalid amount format: '{amount}'. Please enter a valid number."
            )
            return

        # Check for non-finite values
        if not decimal_amount.is_finite():
            views.display_error(
                f"Invalid amount: '{amount}'. Amount must be a finite number."
            )
            return

        # Check for negative values (use case will also validate)
        if decimal_amount < 0:
            views.display_error("Amount cannot be negative.")
            return

        expense = di.get_add_expense_use_case().execute(description, decimal_amount)

        views.display_success(f"Added: {expense.description} for ₦{expense.amount:.2f}")
    except ValueError as e:
        views.display_error(str(e))
    except Exception as e:
        # Catch any unexpected errors (like Decimal issues, storage errors)
        views.display_error(f"An unexpected error occurred: {str(e)}")


@app.command()
def ls():
    """Lists all recorded expenses."""
    try:
        expenses = di.get_list_expenses_use_case().execute()
        views.display_expenses_table(expenses)
    except Exception as e:
        views.display_error(f"Failed to list expenses: {str(e)}")


@app.command()
def delete(expense_id: int):
    """Deletes an expense by its ID."""
    try:
        di.get_delete_expense_use_case().execute(expense_id)
        views.display_success(f"Successfully deleted expense #{expense_id}")
    except ValueError as e:
        views.display_error(str(e))
    except Exception as e:
        views.display_error(f"Failed to delete expense: {str(e)}")
