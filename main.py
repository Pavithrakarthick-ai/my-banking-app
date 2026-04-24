import flet as ft
from datetime import datetime
import os

# --- UNIT V: OOP & CLASS ---
class Account:
    def __init__(self, acc_no, holder, balance=0.0, history=None):
        self.acc_no = acc_no
        self.holder = holder
        self.balance = float(balance)
        self.history = history if history else []

    def deposit(self, amount):
        self.balance += amount
        self.history.append({
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "type": "Deposit",
            "amount": amount
        })
        return f"Deposited: {amount}. New Balance: {self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds!")
        self.balance -= amount
        self.history.append({
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "type": "Withdrawal",
            "amount": amount
        })
        return f"Withdrawn: {amount}. New Balance: {self.balance}"

# Android-la crash aagama irukka file path settings
DATA_FILE = os.path.join(os.getcwd(), "banking_data.txt")

def main(page: ft.Page):
    page.title = "Team 4: Banking System"
    page.scroll = "auto"
    accounts_db = {}

    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) >= 3:
                            acc_no, name, bal = parts[0], parts[1], parts[2]
                            accounts_db[acc_no] = Account(acc_no, name, bal)
            except Exception:
                pass # Crash aagama irukka skip panrom

    def save_data():
        try:
            with open(DATA_FILE, "w") as f:
                for acc in accounts_db.values():
                    f.write(f"{acc.acc_no},{acc.holder},{acc.balance}\n")
        except Exception:
            pass

    load_data()

    # UI Elements
    acc_input = ft.TextField(label="Account Number", width=300)
    name_input = ft.TextField(label="Holder Name", width=300)
    amt_input = ft.TextField(label="Amount", width=300, prefix_text="₹")
    output_text = ft.Text(value="Welcome to Banking System", color="blue", size=16)

    def create_acc_click(e):
        if acc_input.value and name_input.value:
            accounts_db[acc_input.value] = Account(acc_input.value, name_input.value)
            save_data()
            output_text.value = f"Account created for {name_input.value}"
            page.update()

    def deposit_click(e):
        try:
            res = accounts_db[acc_input.value].deposit(float(amt_input.value))
            save_data()
            output_text.value = res
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}"
        page.update()

    def withdraw_click(e):
        try:
            res = accounts_db[acc_input.value].withdraw(float(amt_input.value))
            save_data()
            output_text.value = res
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Secure Banking", size=25, weight="bold"),
            acc_input, name_input, amt_input,
            ft.Row([
                ft.ElevatedButton("Create", on_click=create_acc_click),
                ft.ElevatedButton("Deposit", on_click=deposit_click),
                ft.ElevatedButton("Withdraw", on_click=withdraw_click),
            ]),
            output_text
        ], horizontal_alignment="center")
    )

ft.app(target=main)
