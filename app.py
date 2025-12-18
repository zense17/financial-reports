from nlp_query import interpret
from reports import total_sales, total_expenses, total_profit
from visualize import sales_chart, expenses_chart, profit_chart

def menu():
    print("\nFINANCIAL & SALES REPORTING SYSTEM")
    print("[1] Show Total Sales")
    print("[2] Show Total Expenses")
    print("[3] Show Total Profit")
    print("[4] Charts Menu")
    print("[5] NLP Query")
    print("[0] Exit")

def charts():
    print("\nCharts Menu")
    print("[1] Sales Chart")
    print("[2] Expenses Chart")
    print("[3] Profit Chart")
    choice = input("Enter choice: ")
    if choice == "1":
        sales_chart()
    elif choice == "2":
        expenses_chart()
    elif choice == "3":
        profit_chart()

def run_nlp():
    query = input("Enter your question: ")
    action = interpret(query.lower())
    if action == "show total sales":
        print("Total Sales:", total_sales())
    elif action == "show total expenses":
        print("Total Expenses:", total_expenses())
    elif action == "show profit":
        print("Profit:", total_profit())
    elif action == "sales chart":
        sales_chart()
    elif action == "expense chart":
        expenses_chart()
    elif action == "profit chart":
        profit_chart()

def main():
    while True:
        menu()
        choice = input("Enter: ").strip()
        if choice == "1":
            print("\nTotal Sales:", total_sales())
        elif choice == "2":
            print("\nTotal Expenses:", total_expenses())
        elif choice == "3":
            print("\nProfit:", total_profit())
        elif choice == "4":
            charts()
        elif choice == "5":
            run_nlp()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
