"""REST API for the expense tracker."""

from datetime import date, datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from main import load_expenses, save_expenses


app = FastAPI(title="Expense Tracker API", version="1.0.0")


class Expense(BaseModel):
    date: date
    time: str = Field(pattern=r"^\d{2}:\d{2}$")
    amount: float = Field(gt=0)
    purpose: str = Field(min_length=1)
    category: str = Field(min_length=1)


def as_expense(item):
    """Convert saved JSON data into the API response format."""
    return Expense(
        date=item["date"],
        time=item["time"],
        amount=item["amount"],
        purpose=item["purpose"],
        category=item["category"],
    )


@app.get("/")
def home():
    return {"message": "Expense Tracker API", "docs": "/docs"}


@app.get("/expenses", response_model=list[Expense])
def get_expenses(search: str | None = Query(default=None)):
    expenses = load_expenses()
    if search:
        search = search.lower()
        expenses = [
            expense
            for expense in expenses
            if search in " ".join(str(value).lower() for value in expense.values())
        ]
    return [as_expense(expense) for expense in expenses]


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(expense: Expense):
    expenses = load_expenses()
    new_expense = expense.model_dump()
    new_expense["date"] = expense.date.isoformat()
    expenses.append(new_expense)
    save_expenses(expenses)
    return expense


@app.get("/expenses/summary")
def get_summary():
    expenses = load_expenses()
    by_category = {}
    for expense in expenses:
        category = expense["category"]
        by_category[category] = by_category.get(category, 0) + float(expense["amount"])

    return {
        "total": round(sum(float(expense["amount"]) for expense in expenses), 2),
        "by_category": {
            category: round(amount, 2)
            for category, amount in sorted(by_category.items())
        },
    }


@app.delete("/expenses")
def delete_expenses(confirm: bool = Query(default=False)):
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Pass ?confirm=true to delete all expenses.",
        )
    save_expenses([])
    return {"message": "All expenses deleted."}
