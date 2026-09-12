# expense tracker

## problem

i want to build a simple command - line application
that allows a user to record and manage their expenses

## core features

- add an expense
- view all expenses
- delete all expenses
- search an expenses
- calculate the spending
- show spending by category
- save the expenses so they do not lost when the program is closes

## Run the command-line app

```bash
python main.py
```

## Run the API

Install the packages:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### API endpoints

- `GET /expenses` - view all expenses
- `GET /expenses?search=food` - search expenses
- `POST /expenses` - add an expense
- `GET /expenses/summary` - get total spending and category totals
- `DELETE /expenses?confirm=true` - delete all expenses

## Expense Data

One expense should contain:

- date
- time
- amount
- purpose
- category
