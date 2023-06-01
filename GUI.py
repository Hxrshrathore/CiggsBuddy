import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Global variables to store expense data
monthly_expenses = []
daily_expenses = []

# GUI application
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Create labels and entry fields
        self.num_cigs_label = tk.Label(root, text="Number of Cigarettes:")
        self.num_cigs_entry = tk.Entry(root)
        self.num_cigs_label.pack()
        self.num_cigs_entry.pack()

        self.total_cost_label = tk.Label(root, text="Total Cost (INR):")
        self.total_cost_entry = tk.Entry(root)
        self.total_cost_label.pack()
        self.total_cost_entry.pack()

        # Create buttons
        self.record_button = tk.Button(root, text="Record", command=self.record_expense)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_records)
        self.total_cigs_button = tk.Button(root, text="Total Cigarettes", command=self.total_cigarettes)
        self.total_expenses_button = tk.Button(root, text="Total Expenses", command=self.total_expenses)
        self.compare_button = tk.Button(root, text="Compare", command=self.compare_previous_month)
        self.export_button = tk.Button(root, text="Export to Excel", command=self.export_to_excel)

        self.record_button.pack()
        self.clear_button.pack()
        self.total_cigs_button.pack()
        self.total_expenses_button.pack()
        self.compare_button.pack()
        self.export_button.pack()

    def record_expense(self):
        try:
            num_cigarettes = int(self.num_cigs_entry.get())
            total_cost = float(self.total_cost_entry.get())

            today = datetime.date.today()
            daily_expenses.append(total_cost)
            monthly_expenses.append(total_cost)

            messagebox.showinfo("Expense Recorded", f"Daily expense recorded: {total_cost} INR")

            # Compare with previous day's expense
            if len(daily_expenses) > 1:
                prev_expense = daily_expenses[-2]
                difference = total_cost - prev_expense
                percentage_diff = (difference / prev_expense) * 100

                messagebox.showinfo("Comparison", f"Difference from previous day: {difference} INR ({percentage_diff}%)")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid values for number of cigarettes and total cost.")

        self.num_cigs_entry.delete(0, tk.END)
        self.total_cost_entry.delete(0, tk.END)

    def clear_records(self):
        daily_expenses.clear()
        monthly_expenses.clear()
        messagebox.showinfo("Records Cleared", "All records have been cleared.")

    def total_cigarettes(self):
        total_cigs = sum(daily_expenses)
        messagebox.showinfo("Total Cigarettes", f"Total number of cigarettes: {total_cigs}")

    def total_expenses(self):
        total_expenses = sum(monthly_expenses)
        messagebox.showinfo("Total Expenses", f"Total expenses: {total_expenses} INR")

    def compare_previous_month(self):
        if len(monthly_expenses) < 2:
            messagebox.showwarning("Not Enough Data", "Not enough data to compare with the previous month.")
            return

        this_month_expenses = sum(monthly_expenses[-2:])
        prev_month_expenses = sum(monthly_expenses[:-2])

        difference = this_month_expenses - prev_month_expenses
        percentage_diff = (difference / prev_month_expenses) * 100

        messagebox.showinfo("Comparison", f"Difference from previous month: {difference} INR ({percentage_diff}%)")

    def export_to_excel(self):
        # Create a DataFrame from the data
        data = {'Date': [datetime.date.today() - datetime.timedelta(days=i) for i in range(len(daily_expenses))],
                'Cigarettes': daily_expenses,
                'Expense': daily_expenses}
        df = pd.DataFrame(data)

        # Export the DataFrame to Excel
        filename = 'expense_report.xlsx'
        df.to_excel(filename, index=False)

        messagebox.showinfo("Export Complete", "Expense data exported to Excel.")

# Create the root window
root = tk.Tk()

# Create an instance of the ExpenseTrackerApp
app = ExpenseTrackerApp(root)

# Run the GUI application
root.mainloop()
