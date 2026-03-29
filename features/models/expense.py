from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def get_today() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


@dataclass
class Expense:
    description: str
    amount: float
    date: str = field(default_factory=get_today)
    id: Optional[int] = None

    def __str__(self) -> str:
        expense_id = self.id if self.id is not None else "N/A"
        return f"[{expense_id}] {self.date} | {self.description} | ${self.amount:.2f}"
