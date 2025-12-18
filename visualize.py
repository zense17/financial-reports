import matplotlib.pyplot as plt
from reports import sales_dataframe, expenses_dataframe

def sales_chart():
    df = sales_dataframe()
    df.plot(x="date", y="amount")
    plt.title("Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.show()

def expenses_chart():
    df = expenses_dataframe()
    df.plot(x="date", y="amount", color="red")
    plt.title("Expenses Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.show()

def profit_chart():
    s = sales_dataframe()
    e = expenses_dataframe()
    # Group by date and align indexes
    s_group = s.groupby("date").sum(numeric_only=True)["amount"]
    e_group = e.groupby("date").sum(numeric_only=True)["amount"]
    profit = s_group.subtract(e_group, fill_value=0)

    profit.plot()
    plt.title("Profit Over Time")
    plt.xlabel("Date")
    plt.ylabel("Profit")
    plt.show()
