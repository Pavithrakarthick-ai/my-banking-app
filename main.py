import flet as ft
from datetime import datetime


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
        return f"Deposited: ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}"

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
    page.title = "Banking System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    accounts_db = {}

    def load_data():
        try:
            stored = page.client_storage.get("banking_data")
            if stored and isinstance(stored, dict):
                for acc_no, data in stored.items():
                    accounts_db[acc_no] = Account(
                        acc_no,
                        data.get('name', ''),
                        data.get('balance', 0.0),
                        data.get('history', [])
                    )
        except Exception:
            pass

    def save_data():
        try:
            data_to_save = {
                acc_no: {
                    "name": acc.holder,
                    "balance": acc.balance,
                    "history": acc.history
                }
                for acc_no, acc in accounts_db.items()
            }
            page.client_storage.set("banking_data", data_to_save)
        except Exception:
            pass

    load_data()

    acc_input = ft.TextField(
        label="Account Number",
        border_radius=10,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )
    name_input = ft.TextField(
        label="Account Holder Name",
        border_radius=10,
        width=300
    )
    amt_input = ft.TextField(
        label="Amount",
        prefix_text="₹",
        border_radius=10,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )
    output_text = ft.Text(
        value="Welcome!",
        color=ft.colors.BLUE,
        size=16,
        weight=ft.FontWeight.BOLD
    )
    history_list = ft.Column(controls=[], spacing=5)

    def refresh_history():
        history_list.controls.clear()
        acc_no = acc_input.value.strip()
        if acc_no in accounts_db:
            txns = accounts_db[acc_no].history
            if txns:
                history_list.controls.append(
                    ft.Text("Transaction History", weight=ft.FontWeight.BOLD, size=15)
                )
                for txn in reversed(txns):
                    color = ft.colors.GREEN if txn["type"] == "Deposit" else ft.colors.RED
                    history_list.controls.append(
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{txn['type']}  ₹{txn['amount']:.2f}",
                                        color=color,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(txn["date"], size=11, color=ft.colors.GREY),
                                ],
                                spacing=2
                            ),
                            bgcolor=ft.colors.GREY_100,
                            border_radius=8,
                            padding=10,
                            width=300
                        )
                    )
            else:
                history_list.controls.append(
                    ft.Text("No transactions yet.", color=ft.colors.GREY)
                )
        page.update()

    def create_acc_click(e):
        acc_no = acc_input.value.strip()
        name = name_input.value.strip()
        if acc_no and name:
            if acc_no not in accounts_db:
                accounts_db[acc_no] = Account(acc_no, name)
                save_data()
                output_text.value = f"Account created for {name}!"
                output_text.color = ft.colors.GREEN
            else:
                output_text.value = "Account already exists!"
                output_text.color = ft.colors.ORANGE
        else:
            output_text.value = "Enter account number and name!"
            output_text.color = ft.colors.RED
        refresh_history()

    def deposit_click(e):
        try:
            acc_no = acc_input.value.strip()
            amount = float(amt_input.value.strip())
            if acc_no in accounts_db:
                res = accounts_db[acc_no].deposit(amount)
                save_data()
                output_text.value = res
                output_text.color = ft.colors.GREEN
            else:
                output_text.value = "Account not found!"
                output_text.color = ft.colors.RED
        except ValueError as ex:
            output_text.value = f"Error: {str(ex)}"
            output_text.color = ft.colors.RED
        refresh_history()

    def withdraw_click(e):
        try:
            acc_no = acc_input.value.strip()
            amount = float(amt_input.value.strip())
            if acc_no in accounts_db:
                res = accounts_db[acc_no].withdraw(amount)
                save_data()
                output_text.value = res
                output_text.color = ft.colors.GREEN
            else:
                output_text.value = "Account not found!"
                output_text.color = ft.colors.RED
        except ValueError as ex:
            output_text.value = f"Error: {str(ex)}"
            output_text.color = ft.colors.RED
        refresh_history()

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "🏦 Banking System",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(),
                acc_input,
                name_input,
                ft.ElevatedButton(
                    text="Create Account",
                    on_click=create_acc_click,
                    width=300
                ),
                ft.Divider(),
                amt_input,
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Deposit",
                            on_click=deposit_click,
                            bgcolor=ft.colors.GREEN,
                            color=ft.colors.WHITE,
                            width=130
                        ),
                        ft.ElevatedButton(
                            text="Withdraw",
                            on_click=withdraw_click,
                            bgcolor=ft.colors.RED,
                            color=ft.colors.WHITE,
                            width=130
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.ElevatedButton(
                    text="View History",
                    on_click=lambda e: refresh_history(),
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    width=300
                ),
                output_text,
                ft.Divider(),
                history_list,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )
    )


ft.app(target=main)
