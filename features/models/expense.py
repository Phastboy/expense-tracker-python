from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


def get_today() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return date.today().isoformat()


@dataclass
class Expense:
    description: str
    amount: Decimal
    date: str = field(default_factory=get_today)
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate and normalize amount."""
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))

        self.amount = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if self.amount < 0:
            raise ValueError("Expense amount cannot be negative")

    def __str__(self) -> str:
        expense_id = self.id if self.id is not None else "N/A"
        return f"[{expense_id}] {self.date} | {self.description} | ${self.amount:.2f}"
