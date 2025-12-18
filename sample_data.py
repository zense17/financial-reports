from datetime import date
from db import session, engine
from models import Base, Sales, Expenses

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

sales_entries = [
    Sales(date=date(2025, 1, 1), description="Product A", amount=1500),
    Sales(date=date(2025, 1, 3), description="Product B", amount=2200),
    Sales(date=date(2025, 1, 5), description="Online Order", amount=1800),
]

expense_entries = [
    Expenses(date=date(2025, 1, 2), category="Rent", amount=1000),
    Expenses(date=date(2025, 1, 3), category="Supplies", amount=350),
    Expenses(date=date(2025, 1, 6), category="Electricity", amount=500),
]

session.add_all(sales_entries + expense_entries)
session.commit()
print("Sample Data Inserted!")
