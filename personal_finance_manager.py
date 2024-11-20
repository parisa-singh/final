import tkinter as tk
from tkinter import messagebox, ttk
import json
import matplotlib.pyplot as plt  # type: ignore
import re  # Regular expression module
import os  # Added for file deletion

# Expense class definition
class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def __repr__(self):
        return f"{self.date} | {self.category} | ${self.amount} | {self.description}"

# Global expense and budget data
expenses = []
budgets = {}

# File handling functions
def save_expenses_to_file(expenses, filename="expenses.json"):
    with open(filename, 'w') as file:
        json.dump([expense.__dict__ for expense in expenses], file)

def load_expenses_from_file(filename="expenses.json"):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return [Expense(**item) for item in data]
    except FileNotFoundError:
        return []

def save_budgets_to_file(budgets, filename="budgets.json"):
    with open(filename, 'w') as file:
        json.dump(budgets, file)

def load_budgets_from_file(filename="budgets.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Clear all function - New Addition
def clear_all_data():
    global expenses, budgets
    
    # Ask for confirmation
    if not messagebox.askyesno("Confirm Clear All", 
                              "This will permanently delete all expenses and budgets.\n"
                              "This action cannot be undone.\n\n"
                              "Are you sure you want to continue?"):
        return

    try:
        # Clear memory
        expenses.clear()
        budgets.clear()

        # Delete files
        files_to_delete = ['expenses.json', 'budgets.json']
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

        # Clear all displays
        expense_listbox.delete(0, tk.END)
        total_spending_label.config(text="Total Spending: $0")
        spending_by_category_label.config(text="Spending by Category: ")
        budget_label.config(text="No budget data available.")

        # Clear all entry fields
        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        budget_category_entry.delete(0, tk.END)
        budget_amount_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "All data has been cleared successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while clearing data: {str(e)}")

# Date validation function
def is_valid_date(date_str):
    pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$'
    if not re.match(pattern, date_str):
        return False
    
    day, month, year = map(int, date_str.split('-'))
    
    # Check for valid days in each month
    days_in_month = {
        1: 31, 2: 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    
    return day <= days_in_month[month]

# Analysis functions
def calculate_total_spending():
    return sum(exp.amount for exp in expenses)

def calculate_spending_by_category():
    category_totals = {}
    for exp in expenses:
        if exp.category not in category_totals:
            category_totals[exp.category] = 0
        category_totals[exp.category] += exp.amount
    return category_totals

def plot_spending_distribution():
    if not budgets:
        messagebox.showinfo("No Data", "No budget data available to plot.")
        return
    categories = list(budgets.keys())
    amounts = [sum(exp.amount for exp in expenses if exp.category == cat) for cat in categories]
    if sum(amounts) == 0:
        messagebox.showinfo("No Spending", "No spending data available to plot.")
        return
    plt.figure(figsize=(8, 8))  # Set a fixed size for the plot
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Spending Distribution")
    plt.show()

# Budget checking function
def check_budget_exceeded(category, amount):
    if category in budgets:
        total_spent = sum(exp.amount for exp in expenses if exp.category == category)
        if total_spent + amount > budgets[category]:
            excess = total_spent + amount - budgets[category]
            user_choice = messagebox.askyesno("Budget Exceeded for {category} exceeded by ${excess:.2f}", "Do you still want to add this expense?")
            if not user_choice:
                return

# GUI update functions
def update_expense_listbox():
    expense_listbox.delete(0, tk.END)
    for expense in expenses:
        expense_listbox.insert(tk.END, expense)

def refresh_window():
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

def update_budget_label():
    if budgets:
        budget_data = "\n".join([f"{category}: ${amount:.2f}" for category, amount in budgets.items()])
        budget_label.config(text=budget_data)
    else:
        budget_label.config(text="No budget data available.")

# Action functions
def add_expense():
    date = date_entry.get()
    
    if not is_valid_date(date):
        messagebox.showwarning("Invalid Date", "Please enter a valid date in DD-MM-YYYY format.")
        return
    
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        description = description_entry.get()
        
        if not category:
            messagebox.showwarning("Input Error", "Please enter a category.")
            return
        
        new_expense = Expense(date, amount, category, description)
        expenses.append(new_expense)
        check_budget_exceeded(category, amount)
        update_expense_listbox()
        save_expenses_to_file(expenses)
        refresh_window()
        show_total_spending()  # Update total spending display
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for the amount.")

def update_budget():
    try:
        category = budget_category_entry.get()
        budget = float(budget_amount_entry.get())
        
        if category and budget > 0:
            budgets[category] = budget
            save_budgets_to_file(budgets)
            update_budget_label()
            messagebox.showinfo("Success", f"Budget set for {category}: ${budget:.2f}")
            # Clear budget entry fields
            budget_category_entry.delete(0, tk.END)
            budget_amount_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid category and budget amount.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for the budget amount.")

def show_total_spending():
    total = calculate_total_spending()
    total_spending_label.config(text=f"Total Spending: ${total:.2f}")

def show_spending_by_category():
    spending = calculate_spending_by_category()
    if spending:
        formatted_spending = "\n".join([f"{cat}: ${amt:.2f}" for cat, amt in spending.items()])
        spending_by_category_label.config(text=f"Spending by Category:\n{formatted_spending}")
    else:
        spending_by_category_label.config(text="No spending data available")

def clear_display():
    total_spending_label.config(text="Total Spending: $0")
    spending_by_category_label.config(text="Spending by Category: ")
    expense_listbox.delete(0, tk.END)

def clear_budget_data():
    if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all budget data?"):
        budgets.clear()
        save_budgets_to_file(budgets)
        update_budget_label()
        messagebox.showinfo("Success", "Budget data cleared.")

def show_budget_table():
    if budgets:
        budgets_string = "\n".join([f"{category}: ${budget:.2f}" for category, budget in budgets.items()])
        messagebox.showinfo("Budget Table", budgets_string)
    else:
        messagebox.showinfo("Budget Table", "No budget data available.")

# GUI main window setup
root = tk.Tk()
root.title("Personal Finance Manager")
root.state('zoomed')

# Create main canvas with scrollbar
main_canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = ttk.Frame(main_canvas)

# Configure scrolling
scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
main_canvas.configure(yscrollcommand=scrollbar.set)

# Configure grid weights for centering
for i in range(20):
    scrollable_frame.grid_rowconfigure(i, weight=1)
scrollable_frame.grid_columnconfigure(0, weight=1)


# Load saved data
expenses = load_expenses_from_file()
budgets = load_budgets_from_file()


# Create centered content frame
content_frame = ttk.Frame(scrollable_frame)
content_frame.grid(row=0, column=0, padx=20, pady=20)


# Input fields
ttk.Label(content_frame, text="Date (DD-MM-YYYY):").pack(pady=5)
date_entry = ttk.Entry(content_frame)
date_entry.pack(pady=5)

ttk.Label(content_frame, text="Amount:").pack(pady=5)
amount_entry = ttk.Entry(content_frame)
amount_entry.pack(pady=5)

ttk.Label(content_frame, text="Category:").pack(pady=5)
category_entry = ttk.Entry(content_frame)
category_entry.pack(pady=5)

ttk.Label(content_frame, text="Description:").pack(pady=5)
description_entry = ttk.Entry(content_frame)
description_entry.pack(pady=5)

# Add expense button
add_expense_button = ttk.Button(content_frame, text="Add Expense", command=add_expense)
add_expense_button.pack(pady=10)

# Expense listbox with frame
listbox_frame = ttk.Frame(content_frame)
listbox_frame.pack(pady=10, fill="both", expand=True)
expense_listbox = tk.Listbox(listbox_frame, width=50, height=10)
list_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=expense_listbox.yview)
expense_listbox.configure(yscrollcommand=list_scrollbar.set)
expense_listbox.pack(side="left", fill="both", expand=True)
list_scrollbar.pack(side="right", fill="y")

# Labels for totals
total_spending_label = ttk.Label(content_frame, text="Total Spending: $0")
total_spending_label.pack(pady=5)

spending_by_category_label = ttk.Label(content_frame, text="Spending by Category: ")
spending_by_category_label.pack(pady=5)

# Budget input section
ttk.Label(content_frame, text="Category for Budget:").pack(pady=5)
budget_category_entry = ttk.Entry(content_frame)
budget_category_entry.pack(pady=5)

ttk.Label(content_frame, text="Budget Amount:").pack(pady=5)
budget_amount_entry = ttk.Entry(content_frame)
budget_amount_entry.pack(pady=5)

# Budget display label
budget_label = ttk.Label(content_frame, text="No budget data available.")
budget_label.pack(pady=10)

# Buttons frame
buttons_frame = ttk.Frame(content_frame)
buttons_frame.pack(pady=10)

buttons = [
    ("Set Budget", update_budget),
    ("Show Total Spending", show_total_spending),
    ("Show Spending by Category", show_spending_by_category),
    ("Plot Spending Distribution", plot_spending_distribution),
    ("Clear Display", clear_display),
    ("Clear Budget Data", clear_budget_data),
    ("Show Budget Table", show_budget_table),
    ("Clear All Data", clear_all_data)  # Added Clear All button
]

for text, command in buttons:
    button = ttk.Button(buttons_frame, text=text, command=command)
    button.pack(pady=5, fill="x")
    # Make the Clear All button red and more noticeable
    if text == "Clear All Data":
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red")
        button.configure(style="Red.TButton")

# Pack the main canvas and scrollbar
main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Load existing data
update_expense_listbox()
update_budget_label()
show_total_spending()

# Start the application
root.mainloop()