import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path(__file__).with_name("expenses.json")


def load_expenses():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            expenses = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load expenses: {error}")
        return []

    if not isinstance(expenses, list):
        print("The saved file is not in the right format.")
        return []
    return expenses


def save_expenses(expenses):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=2)
    except OSError as error:
        print(f"Could not save the expenses: {error}")


def get_text(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Please enter something.")


def get_date():
    while True:
        value = input("Date (YYYY-MM-DD, leave blank for today): ").strip()
        if not value:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("That date is not valid.")


def get_time():
    while True:
        value = input("Time (HH:MM, leave blank for now): ").strip()
        if not value:
            return datetime.now().strftime("%H:%M")
        try:
            return datetime.strptime(value, "%H:%M").strftime("%H:%M")
        except ValueError:
            print("That time is not valid.")


def get_amount():
    while True:
        value = input("Amount: ").strip()
        try:
            amount = float(value)
            if amount > 0:
                return round(amount, 2)
        except ValueError:
            pass
        print("Please enter a positive number.")


def show_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n#  Date        Time   Amount       Category       Purpose")
    print("-" * 68)
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<3}{expense['date']:<12}{expense['time']:<7}"
            f"${float(expense['amount']):>9.2f}   "
            f"{str(expense['category'])[:14]:<15}{expense['purpose']}"
        )


def add_expense(expenses):
    print("\nAdd an expense")
    expense = {
        "date": get_date(),
        "time": get_time(),
        "amount": get_amount(),
        "purpose": get_text("Purpose: "),
        "category": get_text("Category: "),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")


def delete_all_expenses(expenses):
    if not expenses:
        print("\nThere are no expenses to delete.")
        return
    confirmation = input("Delete ALL expenses? Type 'yes' to confirm: ").strip().lower()
    if confirmation == "yes":
        expenses.clear()
        save_expenses(expenses)
        print("All expenses deleted.")
    else:
        print("Deletion cancelled.")


def search_expenses(expenses):
    query = get_text("Search by purpose, category, date, or amount: ").lower()
    matches = [
        expense
        for expense in expenses
        if query in " ".join(str(value).lower() for value in expense.values())
    ]
    show_expenses(matches)


def show_summary(expenses):
    total = sum(float(expense["amount"]) for expense in expenses)
    print(f"\nTotal spending: ${total:.2f}")
    if not expenses:
        return

    by_category = {}
    for expense in expenses:
        category = str(expense["category"])
        by_category[category] = by_category.get(category, 0) + float(expense["amount"])

    print("Spending by category:")
    for category, amount in sorted(by_category.items(), key=lambda item: item[0].lower()):
        print(f"  {category}: ${amount:.2f}")


def print_menu() -> None:
    print(
        "\nExpense Tracker\n"
        "1. Add an expense\n"
        "2. View all expenses\n"
        "3. Delete all expenses\n"
        "4. Search expenses\n"
        "5. Calculate spending and show by category\n"
        "6. Exit"
    )


def main() -> None:
    expenses = load_expenses()
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            delete_all_expenses(expenses)
        elif choice == "4":
            search_expenses(expenses)
        elif choice == "5":
            show_summary(expenses)
        elif choice == "6":
            print("Goodbye!")
            return
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
