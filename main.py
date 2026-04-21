import flet as ft
from datetime import datetime

# --- UNIT V: OOP & CLASS ---
class Account:
    def __init__(self, acc_no, holder, balance=0.0, history=None):
        self.acc_no = acc_no
        self.holder = holder
        self.balance = float(balance)
        self.history = history if history else []

    # --- UNIT II: FUNCTIONS (Deposit) ---
    def deposit(self, amount):
        self.balance += amount
        self.history.append({
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "type": "Deposit",
            "amount": amount
        })
        return f"Deposited: ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}"

    # --- UNIT I & VI: CONDITIONS & EXCEPTIONS ---
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds!")
        self.balance -= amount
        self.history.append({
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "type": "Withdraw",
            "amount": amount
        })
        return f"Withdrawn: ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}"


def main(page: ft.Page):
    page.title = "Team 4: Banking System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # --- UNIT III: DICTIONARY (Data Storage) ---
    accounts_db = {}

    # --- UNIT IV: FILE HANDLING (Mobile-kaga client_storage use panrom) ---
    def load_data():
        stored = page.client_storage.get("banking_data")
        if stored:
            for acc_no, data in stored.items():
                accounts_db[acc_no] = Account(
                    acc_no,
                    data['name'],
                    data['balance'],
                    data.get('history', [])
                )

    def save_data():
        data_to_save = {
            acc_no: {
                "name": acc.holder,
                "balance": acc.balance,
                "history": acc.history
            }
            for acc_no, acc in accounts_db.items()
        }
        page.client_storage.set("banking_data", data_to_save)

    load_data()

    # --- UI COMPONENTS ---
    acc_input = ft.TextField(label="Account Number", border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    name_input = ft.TextField(label="Account Holder Name", border_radius=10)
    amt_input = ft.TextField(label="Amount", prefix_text="₹", border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    output_text = ft.Text(value="Welcome!", color="blue", size=16, weight="bold")
    history_list = ft.Column(controls=[], spacing=5)

    def refresh_history():
        history_list.controls.clear()
        acc_no = acc_input.value
        if acc_no in accounts_db:
            txns = accounts_db[acc_no].history
            if txns:
                history_list.controls.append(
                    ft.Text("📋 Transaction History", weight="bold", size=15)
                )
                for txn in reversed(txns):  # Latest first
                    color = "green" if txn["type"] == "Deposit" else "red"
                    icon = "⬆️" if txn["type"] == "Deposit" else "⬇️"
                    history_list.controls.append(
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(f"{icon} {txn['type']}", color=color, width=100),
                                    ft.Text(f"₹{txn['amount']:.2f}", weight="bold", width=100),
                                    ft.Text(txn["date"], size=11, color="grey"),
                                ],
                            ),
                            bgcolor="#f5f5f5",
                            border_radius=8,
                            padding=8,
                        )
                    )
            else:
                history_list.controls.append(
                    ft.Text("No transactions yet.", color="grey")
                )
        page.update()

    def create_acc_click(e):
        if acc_input.value and name_input.value:
            accounts_db[acc_input.value] = Account(acc_input.value, name_input.value)
            save_data()
            output_text.value = f"Account created for {name_input.value}!"
            output_text.color = "green"
            refresh_history()

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
        refresh_history()

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
        refresh_history()

    def view_history_click(e):
        refresh_history()

    # --- UI LAYOUT ---
    page.add(
        ft.SafeArea(
            ft.Column(
                controls=[
                    ft.Text("🏦 Banking System", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                    acc_input,
                    name_input,
                    ft.ElevatedButton(
                        text="Create Account",
                        on_click=create_acc_click,
                        width=300
                    ),
                    amt_input,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Deposit",
                                on_click=deposit_click,
                                bgcolor="green",
                                color="white"
                            ),
                            ft.ElevatedButton(
                                text="Withdraw",
                                on_click=withdraw_click,
                                bgcolor="red",
                                color="white"
                            ),
                            ft.ElevatedButton(
                                text="History",
                                on_click=view_history_click,
                                bgcolor="blue",
                                color="white"
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    output_text,
                    ft.Divider(),
                    history_list,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
    )


ft.app(target=main, view=ft.AppView.FLET_APP)
