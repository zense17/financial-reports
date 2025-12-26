from __future__ import annotations

from datetime import datetime
import json
import difflib

from nlp_query import interpret
from reports import total_sales, total_expenses, total_profit
from visualize import sales_chart, expenses_chart, profit_chart


# -----------------------------
# Innovation 1: Command dispatcher + fuzzy matching
# Innovation 2: Session activity log
# Innovation 3: Export summary to file
# -----------------------------

ACTIVITY_LOG: list[dict] = []


def log_action(action: str, details: str | None = None) -> None:
    ACTIVITY_LOG.append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details or "",
        }
    )


def print_header(title: str) -> None:
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


def menu() -> None:
    print_header("FINANCIAL & SALES REPORTING SYSTEM")
    print("[1] Show Total Sales")
    print("[2] Show Total Expenses")
    print("[3] Show Total Profit")
    print("[4] Charts Menu")
    print("[5] NLP Query")
    print("[6] Show Activity Log (NEW)")
    print("[7] Export Summary Report (NEW)")
    print("[0] Exit")
    print("\nTip: You can also type commands like: sales, expenses, profit, sales chart, export")


def charts_menu() -> None:
    print_header("Charts Menu")
    print("[1] Sales Chart")
    print("[2] Expenses Chart")
    print("[3] Profit Chart")
    print("[0] Back")

    choice = input("Enter choice: ").strip()
    if choice == "1":
        log_action("chart", "sales")
        sales_chart()
    elif choice == "2":
        log_action("chart", "expenses")
        expenses_chart()
    elif choice == "3":
        log_action("chart", "profit")
        profit_chart()


def run_nlp() -> None:
    query = input("Enter your question: ").strip()
    if not query:
        return

    action = interpret(query.lower())
    dispatch_action(action, source="nlp", raw=query)


def show_activity_log() -> None:
    print_header("Activity Log (This Session)")
    if not ACTIVITY_LOG:
        print("No actions yet.")
        return

    for i, item in enumerate(ACTIVITY_LOG, start=1):
        print(f"{i:02d}. [{item['time']}] {item['action']} {('- ' + item['details']) if item['details'] else ''}")


def export_summary() -> None:
    """Exports current totals + session log to a file."""
    print_header("Export Summary Report")

    summary = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totals": {
            "sales": total_sales(),
            "expenses": total_expenses(),
            "profit": total_profit(),
        },
        "activity_log": ACTIVITY_LOG,
    }

    fmt = input("Choose format (1=TXT, 2=JSON): ").strip()
    filename = input("File name (no extension): ").strip() or "report"

    if fmt == "2":
        path = f"{filename}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        log_action("export", path)
        print(f"Saved: {path}")
        return

    # Default TXT
    path = f"{filename}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("FINANCIAL & SALES REPORT SUMMARY\n")
        f.write(f"Generated at: {summary['generated_at']}\n\n")
        f.write(f"Total Sales:    {summary['totals']['sales']}\n")
        f.write(f"Total Expenses: {summary['totals']['expenses']}\n")
        f.write(f"Total Profit:   {summary['totals']['profit']}\n\n")
        f.write("ACTIVITY LOG\n")
        if not ACTIVITY_LOG:
            f.write("No actions recorded.\n")
        else:
            for item in ACTIVITY_LOG:
                f.write(f"[{item['time']}] {item['action']} {item['details']}\n")

    log_action("export", path)
    print(f"Saved: {path}")


# Map "actions" (from NLP or typed commands) to functions
ACTION_MAP = {
    "show total sales": lambda: print("\nTotal Sales:", total_sales()),
    "show total expenses": lambda: print("\nTotal Expenses:", total_expenses()),
    "show profit": lambda: print("\nProfit:", total_profit()),
    "sales chart": sales_chart,
    "expense chart": expenses_chart,
    "profit chart": profit_chart,
}


# Extra shortcuts (Innovation)
SHORTCUTS = {
    "sales": "show total sales",
    "expenses": "show total expenses",
    "expense": "show total expenses",
    "profit": "show profit",
    "sales chart": "sales chart",
    "expenses chart": "expense chart",
    "expense chart": "expense chart",
    "profit chart": "profit chart",
    "log": "show log",
    "activity": "show log",
    "export": "export",
    "help": "help",
}


def best_match(user_text: str, candidates: list[str]) -> str | None:
    """Fuzzy match user input to a candidate command."""
    matches = difflib.get_close_matches(user_text, candidates, n=1, cutoff=0.55)
    return matches[0] if matches else None


def dispatch_action(action: str | None, source: str, raw: str | None = None) -> None:
    if not action:
        print("Sorry, I didn’t understand that.")
        return

    # Handle built-in actions not in ACTION_MAP
    if action == "show log":
        log_action("log", f"source={source}")
        show_activity_log()
        return

    if action == "export":
        log_action("export_menu", f"source={source}")
        export_summary()
        return

    if action == "help":
        log_action("help", f"source={source}")
        print("\nCommands you can type:")
        print("- sales | expenses | profit")
        print("- sales chart | expense chart | profit chart")
        print("- log | export | help")
        print("You can also use menu numbers.")
        return

    func = ACTION_MAP.get(action)
    if not func:
        print(f"Action not supported: {action}")
        return

    log_action(action, f"source={source}" + (f", raw='{raw}'" if raw else ""))
    func()


def main() -> None:
    while True:
        menu()
        choice = input("Enter (number or command): ").strip().lower()

        # Classic menu
        if choice == "1":
            dispatch_action("show total sales", source="menu")
        elif choice == "2":
            dispatch_action("show total expenses", source="menu")
        elif choice == "3":
            dispatch_action("show profit", source="menu")
        elif choice == "4":
            charts_menu()
        elif choice == "5":
            run_nlp()
        elif choice == "6":
            dispatch_action("show log", source="menu")
        elif choice == "7":
            dispatch_action("export", source="menu")
        elif choice == "0":
            log_action("exit")
            break

        # New: command mode
        else:
            if not choice:
                continue

            # Shortcut direct
            if choice in SHORTCUTS:
                dispatch_action(SHORTCUTS[choice], source="typed", raw=choice)
                continue

            # Try fuzzy match on shortcuts keys
            candidate_keys = list(SHORTCUTS.keys())
            match = best_match(choice, candidate_keys)
            if match:
                print(f"Did you mean: '{match}'? Running it...")
                dispatch_action(SHORTCUTS[match], source="fuzzy", raw=choice)
                continue

            # Fall back to NLP interpret
            action = interpret(choice)
            dispatch_action(action, source="typed_nlp", raw=choice)

if __name__ == "__main__":
    main()
