import flet as ft
import os

# --- UNIT V: OOP & CLASS ---
class Account:
    def __init__(self, acc_no, holder, balance=0):
        self.acc_no = acc_no
        self.holder = holder
        self.balance = float(balance)

    def deposit(self, amount):
        self.balance += amount
        return f"Deposited: {amount}. New Balance: {self.balance}"

    # --- UNIT I & VI: CONDITIONS & EXCEPTIONS ---
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds!")
        self.balance -= amount
        return f"Withdrawn: {amount}. New Balance: {self.balance}"

# --- MAIN APP UI ---
def main(page: ft.Page):
    page.title = "Team 4: Banking System"
    page.theme_mode = "light"
    
    # --- UNIT III: DICTIONARY (Data Storage) ---
    accounts_db = {} 

    # --- UNIT IV: FILE HANDLING (Read) ---
    def load_data():
        if os.path.exists("banking_data.txt"):
            with open("banking_data.txt", "r") as f:
                for line in f:
                    acc_no, name, bal = line.strip().split(",")
                    accounts_db[acc_no] = Account(acc_no, name, bal)

    def save_data():
        with open("banking_data.txt", "w") as f:
            for acc in accounts_db.values():
                f.write(f"{acc.acc_no},{acc.holder},{acc.balance}\n")

    load_data()

    # --- UI COMPONENTS ---
    acc_input = ft.TextField(label="Account Number", width=300)
    name_input = ft.TextField(label="Account Holder Name", width=300)
    amt_input = ft.TextField(label="Amount", width=300, prefix_text="?")
    output_text = ft.Text(value="Welcome! Enter details.", color="blue", size=18)

    # --- UNIT II: FUNCTIONS (Transactions) ---
    def create_acc_click(e):
        acc_no = acc_input.value
        name = name_input.value
        if acc_no and name:
            accounts_db[acc_no] = Account(acc_no, name)
            save_data()
            output_text.value = f"Account created for {name}!"
            page.update()

    def deposit_click(e):
        try:
            acc_no = acc_input.value
            amount = float(amt_input.value)
            res = accounts_db[acc_no].deposit(amount)
            save_data()
            output_text.value = res
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}"
        page.update()

    def withdraw_click(e):
        try:
            acc_no = acc_input.value
            amount = float(amt_input.value)
            res = accounts_db[acc_no].withdraw(amount)
            save_data()
            output_text.value = res
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}" # ERROR HANDLING
        page.update()

    # --- ADDING TO PAGE ---
    page.add(
        ft.Column([
            ft.Text("Secure Banking System", size=30, weight="bold"),
            acc_input,
            name_input,
            amt_input,
            ft.Row([
                ft.ElevatedButton("Create Account", on_click=create_acc_click),
                ft.ElevatedButton("Deposit", on_click=deposit_click),
                ft.ElevatedButton("Withdraw", on_click=withdraw_click),
            ]),
            output_text
        ], alignment="center", horizontal_alignment="center")
    )

ft.app(target=main)