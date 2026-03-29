# Expense Tracker CLI 💰

A mathematically accurate, professional-grade Command Line Interface (CLI) for tracking personal expenses. 

Built with modern Python tooling, this application strictly adheres to **Clean Architecture (Ports and Adapters)** to completely decouple business logic from data storage.

## ✨ Features
* **Stateless CLI Design:** Uses `Typer` for native command routing, bypassing clunky `while True` loops for a true terminal experience.
* **Financial Accuracy:** Utilizes Python's `Decimal` module to prevent floating-point rounding errors.
* **Beautiful UI:** Uses `Rich` to render perfectly aligned, colorful terminal tables.
* **Persistent Storage:** Safely serializes models to `expenses.json`.
* **Robust Validation:** Prevents negative amounts, empty descriptions, and invalid IDs.

## 🚀 Prerequisites & Installation

This project utilizes [uv](https://github.com/astral-sh/uv), the lightning-fast Python package and project manager written in Rust, to handle virtual environments and dependencies automatically.

1. **Install `uv` (if not already installed):**
   ```bash
   curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
   ```
   *(Alternatively, use `brew install uv` on macOS).*

2. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/expense-tracker-python.git](https://github.com/Phastboy/expense-tracker-python.git)
   cd expense-tracker-python
   ```

## 💻 Usage

Because `uv` handles the virtual environment natively, you do not need to manually activate anything. Simply use `uv run python main.py` followed by your command.

**View the Help Menu:**
```bash
uv run python main.py --help
```

**Add an Expense:**
```bash
uv run python main.py add "Coffee" 4.50
uv run python main.py add "Groceries" 45.00
```

**List All Expenses:**
```bash
uv run python main.py ls
```

**Delete an Expense:**
```bash
uv run python main.py delete 1
```

## 🏗️ Architecture
This project is structured using Domain-Driven Design principles:
* `features/models/`: Contains the pure `Expense` dataclass.
* `features/store/ports/`: Defines the abstract `ExpenseStore` interface.
* `features/store/adapters/`: Contains the concrete `JsonExpenseStore` implementation.
* `features/use_cases/`: Enforces strict business rules before touching the database.
* `cli/`: The presentation layer handling user input and `Rich` table rendering.

---
