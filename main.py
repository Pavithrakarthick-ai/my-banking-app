import flet as ft

class Account:
    def __init__(self, acc_no, holder, balance=0.0):
        self.acc_no = acc_no
        self.holder = holder
        self.balance = float(balance)

    def deposit(self, amount):
        self.balance += amount
        return f"Deposited: ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}"

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds!")
        self.balance -= amount
        return f"Withdrawn: ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}"

def main(page: ft.Page):
    page.title = "Team 4: Banking System"
    page.theme_mode = "light"
    page.padding = 20
    page.scroll = "auto"
    
    accounts_db = {}

    def load_data():
        stored_data = page.client_storage.get("banking_data")
        if stored_data:
            for acc_no, details in stored_data.items():
                accounts_db[acc_no] = Account(acc_no, details['name'], details['balance'])

    def save_data():
        data_to_store = {
            acc_no: {"name": acc.holder, "balance": acc.balance}
            for acc_no, acc in accounts_db.items()
        }
        page.client_storage.set("banking_data", data_to_store)

    load_data()

    acc_input = ft.TextField(label="Account Number", border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    name_input = ft.TextField(label="Account Holder Name", border_radius=10)
    amt_input = ft.TextField(label="Amount", prefix_text="₹", border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    output_text = ft.Text(value="Welcome!", color="blue", size=16, weight="bold", text_align="center")

    def create_acc_click(e):
        if acc_input.value and name_input.value:
            accounts_db[acc_input.value] = Account(acc_input.value, name_input.value)
            save_data()
            output_text.value = f"Account created for {name_input.value}!"
            output_text.color = "green"
            page.update()

    def deposit_click(e):
        try:
            acc_no = acc_input.value
            amount = float(amt_input.value)
            if acc_no in accounts_db:
                res = accounts_db[acc_no].deposit(amount)
                save_data()
                output_text.value = res
                output_text.color = "green"
            else:
                output_text.value = "Account not found!"
                output_text.color = "red"
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}"
            output_text.color = "red"
        page.update()

    def withdraw_click(e):
        try:
            acc_no = acc_input.value
            amount = float(amt_input.value)
            if acc_no in accounts_db:
                res = accounts_db[acc_no].withdraw(amount)
                save_data()
                output_text.value = res
                output_text.color = "green"
            else:
                output_text.value = "Account not found!"
                output_text.color = "red"
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}"
            output_text.color = "red"
        page.update()

    page.add(
        ft.SafeArea(
            ft.Column(, alignment="center", spacing=10),
                output_text
            ], horizontal_alignment="center", spacing=15)
        )
    )

ft.app(target=main, view=ft.AppView.FLET_APP)
