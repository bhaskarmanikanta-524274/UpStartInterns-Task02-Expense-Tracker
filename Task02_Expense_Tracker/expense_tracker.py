import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("expenses.csv")
FIELDS = ["date", "category", "amount"]

def validate_date(value):
    try: datetime.strptime(value, "%Y-%m-%d"); return True
    except ValueError: return False

def validate_amount(value):
    try: return float(value) > 0
    except ValueError: return False

def load_expenses():
    if not CSV_FILE.exists(): return []
    try:
        with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
            return [r for r in csv.DictReader(f) if all(x in r for x in FIELDS)]
    except (OSError, csv.Error): return []

def save_expense(row):
    exists = CSV_FILE.exists()
    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists: w.writeheader()
        w.writerow(row)

def totals_by_category(rows):
    totals = defaultdict(float)
    for row in rows: totals[row["category"]] += float(row["amount"])
    return dict(totals)

def add_expense():
    date = input("Date (YYYY-MM-DD): ").strip()
    if not validate_date(date): print("Invalid date. Use YYYY-MM-DD."); return
    category = input("Category: ").strip()
    if not category: print("Category cannot be empty."); return
    amount = input("Amount: ").strip()
    if not validate_amount(amount): print("Invalid amount. Enter a number greater than 0."); return
    save_expense({"date": date, "category": category, "amount": f"{float(amount):.2f}"})
    print("Expense saved successfully.")

def show_summary():
    rows = load_expenses()
    if not rows: print("No expenses recorded."); return
    totals = totals_by_category(rows)
    print("\n--- Spending by Category ---")
    for category, total in sorted(totals.items()): print(f"{category}: ${total:.2f}")
    print(f"Total Spending: ${sum(totals.values()):.2f}")

def main():
    while True:
        print("\n=== Expense Tracker ===\n1. Add expense\n2. Show summary\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1": add_expense()
        elif choice == "2": show_summary()
        elif choice == "3": break
        else: print("Invalid choice.")

if __name__ == "__main__": main()
