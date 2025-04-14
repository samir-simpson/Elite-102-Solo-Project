import tkinter as tk 
from tkinter import messagebox
from database import register, verify, check_balance, create_database, deposit, withdraw, delete_account, modfify_account 
create_database()
#This function will create the GUI for the banking app
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking App")
        self.root.geometry("400x400")
        self.user_id = None

        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="PIN").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="PIN").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()

        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def dashboard(self):
        self.clear_screen()

        tk.Label(self.root, text="Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit", command=self.deposit_screen).pack(pady=5)
        tk.Button(self.root, text="Withdraw", command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.root, text="Modify Account", command=self.modify_screen).pack(pady=5)
        tk.Button(self.root, text="Delete Account", command=self.delete_account).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)
    
    def modify_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Modify Account", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="New Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="New PIN").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()

        tk.Button(self.root, text="Modify", command=self.modify_account).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.dashboard).pack()
         
    def deposit_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Deposit", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Amount").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        tk.Button(self.root, text="Deposit", command=self.deposit).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.dashboard).pack()

    def withdraw_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Withdraw", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Amount").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        tk.Button(self.root, text="Withdraw", command=self.withdraw).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.dashboard).pack()

    def login(self):
        username = self.username_entry.get()
        pin = self.pin_entry.get()

        user_id = verify(username, pin)
        if user_id:
            self.user_id = user_id
            messagebox.showinfo("Success", "Login successful!")
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or PIN")

    def register(self):
        username = self.username_entry.get()
        pin = self.pin_entry.get()

        result = register(username, pin)
        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            self.login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    def check_balance(self):
        result = check_balance(self.user_id)
        if result["success"]:
            messagebox.showinfo("Balance", f"Your balance is: ${result['balance']:.2f}")
        else:
            messagebox.showerror("Error", result["message"])

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            result = deposit(self.user_id, amount)
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                self.dashboard()
            else:
                messagebox.showerror("Error", result["message"])
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            result = withdraw(self.user_id, amount)
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                self.dashboard()
            else:
                messagebox.showerror("Error", result["message"])
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def delete_account(self):
        result = delete_account(self.user_id)
        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            self.login_screen()
        else:
            messagebox.showerror("Error", result["message"])

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()