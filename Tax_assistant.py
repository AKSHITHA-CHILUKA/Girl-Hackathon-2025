import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import hashlib  # For password encryption

# Database Setup
conn = sqlite3.connect("tax_data.db")
cursor = conn.cursor()

# Drop the old tax_records table if it exists (to avoid conflicts)
cursor.execute("DROP TABLE IF EXISTS tax_records")

# Create the users table and the new tax_records table with the 'assessment_year' column
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS tax_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    income FLOAT,
    tax FLOAT,
    assessment_year TEXT,  -- New column added
    taxpayer_category TEXT,
    residential_status TEXT
)
""")
conn.commit()

# ---------------------- User Authentication ----------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    username = entry_username.get()
    password = hash_password(entry_password.get())
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("Login Success", "Welcome back!")
        auth_root.destroy()
        main_app(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def register():
    username = entry_username.get()
    password = hash_password(entry_password.get())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration Successful", "You can now log in!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# ---------------------- Tax Calculation Logic ----------------------
def calculate_tax(income, age_group):
    """
    Calculate tax based on income and age group.
    :param income: Annual income (float)
    :param age_group: Age group (str) - "below_60", "60_to_80", "above_80"
    :return: Tax liability (float)
    """
    if income <= 1200000:  # No tax for income up to ₹12,00,000
        return 0

    tax = 0

    if age_group == "below_60":
        if income <= 300000:
            tax = 0
        elif income <= 700000:
            tax = (income - 300000) * 0
        elif income <= 1000000:
            tax = 20000 + (income - 700000) * 0
        elif income <= 1200000:
            tax = 50000 + (income - 1000000) * 0.15
        elif income <= 1500000:
            tax = 80000 + (income - 1200000) * 0.20
        elif income <= 5000000:
            tax = 140000 + (income - 1500000) * 0.30
        elif income <= 10000000:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.10  # Surcharge
        elif income <= 20000000:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.15  # Surcharge
        else:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.25  # Surcharge

    elif age_group == "60_to_80":
        if income <= 300000:
            tax = 0
        elif income <= 700000:
            tax = (income - 300000) * 0
        elif income <= 1000000:
            tax = 20000 + (income - 700000) * 0
        elif income <= 1200000:
            tax = 50000 + (income - 1000000) * 0.15
        elif income <= 1500000:
            tax = 80000 + (income - 1200000) * 0.20
        elif income <= 5000000:
            tax = 140000 + (income - 1500000) * 0.30
        elif income <= 10000000:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.10  # Surcharge
        elif income <= 20000000:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.15  # Surcharge
        else:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.25  # Surcharge

    elif age_group == "above_80":
        if income <= 300000:
            tax = 0
        elif income <= 700000:
            tax = (income - 300000) * 0.05
        elif income <= 1000000:
            tax = 20000 + (income - 700000) * 0.10
        elif income <= 1200000:
            tax = 50000 + (income - 1000000) * 0.15
        elif income <= 1500000:
            tax = 80000 + (income - 1200000) * 0.20
        elif income <= 5000000:
            tax = 140000 + (income - 1500000) * 0.30
        elif income <= 10000000:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.10  # Surcharge
        elif income <= 20000000:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.15  # Surcharge
        else:
            tax = 140000 + (income - 1500000) * 0.30
            tax += tax * 0.25  # Surcharge

    else:
        raise ValueError("Invalid age group. Choose 'below_60', '60_to_80', or 'above_80'.")

    return tax

# ---------------------- Main Tax Calculator ----------------------
def calculate_tax_gui(username, entry_income, result_var, age_group_var, entry_year, category_var, status_var):
    try:
        income = float(entry_income.get())
        tax = calculate_tax(income, age_group_var.get())
        result_var.set(f"Calculated Tax: ₹{tax:,.2f}")

        assessment_year = entry_year.get()
        taxpayer_category = category_var.get()
        residential_status = status_var.get()

        cursor.execute("INSERT INTO tax_records (username, income, tax, assessment_year, taxpayer_category, residential_status) VALUES (?, ?, ?, ?, ?, ?)", 
                      (username, income, tax, assessment_year, taxpayer_category, residential_status))
        conn.commit()
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

# ---------------------- Chat with AI Function ----------------------
def chat_with_ai():
    # Placeholder function for chat functionality
    messagebox.showinfo("Chat with AI", "Chat feature will be added soon!")

# ---------------------- GUI Setup ----------------------

def main_app(username):
    root = ctk.CTk()
    root.title("Tax Assistant")
    root.geometry("500x500")

    ctk.CTkLabel(root, text=f"Welcome, {username}", font=("Arial", 20)).pack(pady=10)

    ctk.CTkLabel(root, text="Assessment Year:").pack(pady=5)
    entry_year = ctk.CTkEntry(root)
    entry_year.insert(0, "2024-25")
    entry_year.pack(pady=5)

    ctk.CTkLabel(root, text="Taxpayer Category:").pack(pady=5)
    category_var = tk.StringVar(value="Individual")
    category_menu = ctk.CTkOptionMenu(root, variable=category_var, values=["Individual", "Company"])
    category_menu.pack(pady=5)

    ctk.CTkLabel(root, text="Residential Status:").pack(pady=5)
    status_var = tk.StringVar(value="RES")
    status_menu = ctk.CTkOptionMenu(root, variable=status_var, values=["RES", "NR"])
    status_menu.pack(pady=5)

    ctk.CTkLabel(root, text="Annual Income (₹)").pack(pady=5)
    entry_income = ctk.CTkEntry(root)
    entry_income.pack(pady=5)

    ctk.CTkLabel(root, text="Age Group").pack(pady=5)
    age_group_var = tk.StringVar(value="below_60")
    ctk.CTkRadioButton(root, text="Below 60", variable=age_group_var, value="below_60").pack()
    ctk.CTkRadioButton(root, text="60 to 80", variable=age_group_var, value="60_to_80").pack()
    ctk.CTkRadioButton(root, text="Above 80", variable=age_group_var, value="above_80").pack()

    result_var = tk.StringVar()
    ctk.CTkLabel(root, textvariable=result_var, font=("Arial", 14), text_color="green").pack(pady=5)

    ctk.CTkButton(root, text="Calculate Tax", command=lambda: calculate_tax_gui(username, entry_income, result_var, age_group_var, entry_year, category_var, status_var)).pack(pady=10)

    ctk.CTkButton(root, text="Chat with AI", command=chat_with_ai).pack(pady=10)

    disclaimer = ctk.CTkLabel(root, text="Disclaimer: This calculator is for basic estimates. Please refer to tax laws for accurate filing.", font=("Arial", 10), text_color="red")
    disclaimer.pack(pady=10)

    root.mainloop()

# ---------------------- Login/Signup UI ----------------------
auth_root = tk.Tk()
auth_root.title("Login / Register")
auth_root.geometry("400x300")

tk.Label(auth_root, text="Tax Assistant Login", font=("Arial", 16)).pack(pady=10)

tk.Label(auth_root, text="Username:").pack()
entry_username = tk.Entry(auth_root)
entry_username.pack(pady=5)

tk.Label(auth_root, text="Password:").pack()
entry_password = tk.Entry(auth_root, show="*")
entry_password.pack(pady=5)

tk.Button(auth_root, text="Login", command=login).pack(pady=5)
tk.Button(auth_root, text="Register", command=register).pack(pady=5)

auth_root.mainloop()