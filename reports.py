import pandas as pd
from db import session
from models import Sales, Expenses

def total_sales():
    df = pd.read_sql(session.query(Sales).statement, session.bind)
    return df.amount.sum()

def total_expenses():
    df = pd.read_sql(session.query(Expenses).statement, session.bind)
    return df.amount.sum()

def total_profit():
    return total_sales() - total_expenses()

def sales_dataframe():
    return pd.read_sql(session.query(Sales).statement, session.bind)

def expenses_dataframe():
    return pd.read_sql(session.query(Expenses).statement, session.bind)
