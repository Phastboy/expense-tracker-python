from rich.console import Console
from rich.table import Table
from features.models.expense import Expense

console = Console()


def display_expenses_table(expenses: list[Expense]) -> None:
    """Renders a beautiful, formatted table of expenses."""
    if not expenses:
        console.print(
            "[yellow]No expenses found. You're either a budgeting master, or completely broke! 😅[/yellow]"
        )
        return

    # Create the table canvas
    table = Table(
        title="💰 Expense Tracker", show_header=True, header_style="bold magenta"
    )

    # Define columns
    table.add_column("ID", style="dim", width=6)
    table.add_column("Date", justify="center")
    table.add_column("Description")
    table.add_column("Amount", justify="right", style="green")

    # Add rows
    for expense in expenses:
        table.add_row(
            str(expense.id), expense.date, expense.description, f"₦{expense.amount:.2f}"
        )

    console.print(table)


def display_success(message: str) -> None:
    console.print(f"[bold green]✔[/bold green] {message}")


def display_error(message: str) -> None:
    console.print(f"[bold red]✘ Error:[/bold red] {message}")
