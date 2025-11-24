import tkinter as tk
from tkinter import messagebox
import os
import datetime

#Configuration
FILENAME = "finance_data.txt"
TRANSACTIONS = []

#Data handling functions
def load_data(filename):
    transactions = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        transactions.append({
                            'date': parts[0],
                            'type': parts[1],
                            'amount': float(parts[2]),
                            'description': parts[3]
                        })
            messagebox.showinfo("Data Load", f"Data loaded successfully from {filename}.")
        except Exception:
            messagebox.showerror("Data Error", "Error loading data. Starting with a fresh list.")
    else:
        messagebox.showinfo("Data Info", f"{filename} not found. Starting with an empty budget.")
    return transactions
def save_data(transactions, filename):
    try:
        with open(filename, 'w') as file:
            for t in transactions:
                line = f"{t['date']}|{t['type']}|{t['amount']}|{t['description']}\n"
                file.write(line)
        messagebox.showinfo("Data Save", f"Data saved successfully to {filename}.")
    except Exception as e:
        messagebox.showerror("Data Error", f"Error saving data: {e}")

#Utility functions
def calculate_balance(transactions):
    total_balance = 0.0
    for t in transactions:
        amount = t['amount']
        if t['type'] == 'Income':
            total_balance += amount
        elif t['type'] == 'Expense':
            total_balance -= amount
    return total_balance
def save_and_exit(root):
    global TRANSACTIONS
    if messagebox.askyesno("Exit", "Do you want to save data before exiting?"):
        save_data(TRANSACTIONS, FILENAME)
    root.destroy()

#UI functions
def update_display(text_widget):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, "--- TRANSACTION HISTORY ---\n", 'header')
    text_widget.insert(tk.END, f"{'Date':<12} {'Type':<8} {'Amount':>12} {'Description':<30}\n", 'subheader')
    text_widget.insert(tk.END, "-" * 65 + "\n")
    for t in TRANSACTIONS:
        amount_str = f"{t['amount']:,.2f}"
        tag = 'income' if t['type'] == 'Income' else 'expense'
        text_widget.insert(tk.END, f"{t['date']:<12} {t['type']:<8} ", 'normal')
        text_widget.insert(tk.END, f"{amount_str:>12} ", tag)
        text_widget.insert(tk.END, f"{t['description']:<30}\n", 'normal')

    balance = calculate_balance(TRANSACTIONS)
    balance_tag = 'balance_pos' if balance >= 0 else 'balance_neg'
    
    text_widget.insert(tk.END, "\n" + "=" * 65 + "\n")
    text_widget.insert(tk.END, f"NET BALANCE: ", 'balance_header')
    text_widget.insert(tk.END, f"Rs.{balance:,.2f}\n", balance_tag)
    text_widget.insert(tk.END, "=" * 65 + "\n")
    text_widget.config(state=tk.DISABLED)
def submit_transaction(type_var, date_entry, amount_entry, desc_entry, text_widget):
    t_type = type_var.get()
    t_date = date_entry.get()
    t_desc = desc_entry.get().strip()
    if not t_type or not t_date or not t_desc:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return
    try:
        t_amount = float(amount_entry.get())
        if t_amount <= 0:
            messagebox.showerror("Input Error", "Amount must be positive.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a valid number.")
        return
    try:
        datetime.datetime.strptime(t_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
        return
    
    new_transaction = {
        'date': t_date,
        'type': t_type,
        'amount': t_amount,
        'description': t_desc
    }
    TRANSACTIONS.append(new_transaction)
    
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    update_display(text_widget)
    messagebox.showinfo("Success", "Transaction recorded successfully.")

#Application functions
def create_main_window():
    global TRANSACTIONS
    root = tk.Tk()
    root.title("Python Finance Manager")
    root.geometry("800x600")
    TRANSACTIONS = load_data(FILENAME)
    input_frame = tk.Frame(root, padx=10, pady=10, bd=2, relief=tk.GROOVE)
    input_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(input_frame, text="NEW TRANSACTION", font=('Arial', 12, 'bold')).grid(row=0, columnspan=2, pady=5)
    tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W)
    date_entry = tk.Entry(input_frame)
    date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
    date_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)
    type_var = tk.StringVar(value='Expense')
    tk.Label(input_frame, text="Type:").grid(row=2, column=0, sticky=tk.W)
    tk.Radiobutton(input_frame, text="Income", variable=type_var, value="Income").grid(row=2, column=1, sticky=tk.W)
    tk.Radiobutton(input_frame, text="Expense", variable=type_var, value="Expense").grid(row=2, column=1, padx=80, sticky=tk.W)
    tk.Label(input_frame, text="Amount:").grid(row=3, column=0, sticky=tk.W)
    amount_entry = tk.Entry(input_frame)
    amount_entry.grid(row=3, column=1, padx=5, pady=2, sticky=tk.EW)
    tk.Label(input_frame, text="Description:").grid(row=4, column=0, sticky=tk.W)
    desc_entry = tk.Entry(input_frame)
    desc_entry.grid(row=4, column=1, padx=5, pady=2, sticky=tk.EW)
    display_frame = tk.Frame(root, padx=10, pady=10, bd=2, relief=tk.GROOVE)
    display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    data_display = tk.Text(display_frame, wrap=tk.WORD, font=('Courier', 10), state=tk.DISABLED)
    data_display.pack(fill=tk.BOTH, expand=True)
    data_display.tag_config('header', font=('Arial', 12, 'bold'), foreground='navy')
    data_display.tag_config('subheader', font=('Courier', 10, 'bold'), foreground='darkblue')
    data_display.tag_config('income', foreground='green', font=('Courier', 10, 'bold'))
    data_display.tag_config('expense', foreground='red', font=('Courier', 10, 'bold'))
    data_display.tag_config('balance_header', font=('Arial', 12, 'bold'), foreground='purple')
    data_display.tag_config('balance_pos', font=('Arial', 14, 'bold'), foreground='green')
    data_display.tag_config('balance_neg', font=('Arial', 14, 'bold'), foreground='red')
    btn_frame = tk.Frame(input_frame)
    btn_frame.grid(row=5, columnspan=2, pady=10)
    submit_btn = tk.Button(btn_frame, text="Record Transaction", bg='lightblue', 
                           command=lambda: submit_transaction(type_var, date_entry, amount_entry, desc_entry, data_display))
    submit_btn.pack(side=tk.LEFT, padx=10)
    update_btn = tk.Button(btn_frame, text="Refresh Display", command=lambda: update_display(data_display))
    update_btn.pack(side=tk.LEFT, padx=10)
    exit_btn = tk.Button(btn_frame, text="Exit & Save", bg='salmon', 
                         command=lambda: save_and_exit(root))
    exit_btn.pack(side=tk.LEFT, padx=10)
    update_display(data_display)
    root.protocol("WM_DELETE_WINDOW", lambda: save_and_exit(root))
    root.mainloop()

#Main
if __name__ == "__main__":
    try:
        create_main_window()
    except Exception as e:
        print(f"\nFATAL APPLICATION ERROR: {e}")
