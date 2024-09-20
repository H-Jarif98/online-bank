import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
EXCEL_FILE = 'bank.xlsx'
if not os.path.exists(EXCEL_FILE):
    df_accounts = pd.DataFrame(columns=['username', 'password', 'balance', 'transactions'])
    df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)
else:
    df_accounts = pd.read_excel(EXCEL_FILE, sheet_name='accounts')

class BankAccount:
    def __init__(self, name, balance=0, transactions=[]):
        self.name = name
        self.balance = balance
        self.transactions = transactions

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount:.2f}")
            return f"Deposited ${amount:.2f}. Current balance: ${self.balance:.2f}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            fee = amount * 0.03
            net_amount = amount - fee
            self.balance -= amount
            self.transactions.append(f"Withdrawn ${amount:.2f} (3% fee: ${fee:.2f}). Net: ${net_amount:.2f}")
            return f"Withdrawn ${amount:.2f}. Fee: ${fee:.2f}. Net: ${net_amount:.2f}. Current balance: ${self.balance:.2f}"
        return "Insufficient funds or invalid withdrawal amount."

    def get_balance(self):
        return self.balance

class BankApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jarif's Bank")
        self.current_account = None
        self.init_main_menu()

    def init_main_menu(self):
            self.clear_screen()
            self.create_navigation_bar('Home')
            header_frame = tk.Frame(self.master)
            header_frame.pack(pady=10)
        
            tk.Label(header_frame, text="Jarif's", font=("Helvetica", 30, "bold"), fg="grey").pack(side="left", padx=10)
            tk.Label(header_frame, text="Bank", font=("Helvetica", 30, "bold"), fg="red").pack(side="left")
            nav_frame = tk.Frame(self.master, bg="#008080")
            nav_frame.pack(fill="x")

        
            self.create_main_menu_box("Deposit Money", self.require_login(self.show_deposit_screen)).pack(side="left", padx=10, pady=20)
            self.create_main_menu_box("Withdraw Money", self.require_login(self.show_withdraw_screen)).pack(side="left", padx=10, pady=20)
            self.create_main_menu_box("Transaction History", self.require_login(self.show_transaction_history)).pack(side="left", padx=10, pady=20)
            self.create_main_menu_box("Apply For Loan", self.require_login(self.show_loan_screen)).pack(side="left", padx=10, pady=20)
            self.create_main_menu_box("Account Management", self.require_login(self.show_account_management)).pack(side="left", padx=15, pady=50)
            self.create_main_menu_box("Transfer Money", self.require_login(self.show_transfer_screen)).pack(side="right", padx=10, pady=20)
            self.create_main_menu_box("Loan management",self.require_login(self.show_loan_management_screen)).pack(side="right", padx= 20, pady=10)
            tk.Label(self.master, text="Build your future with Khondokar Bank", font=("Helvetica", 20, "bold", )).pack(side="bottom", padx= 0 ,pady=10)
        
            if self.current_account:
                self.update_account_info()


    def create_main_menu_box(self, text, command):
        return tk.Button(self.master, text=text, command=command, font=("Helvetica", 10, "bold"), width=15, height=10)

    def create_navigation_bar(self, active):
        frame = tk.Frame(self.master, bg='#004c61')
        frame.pack(fill='x')
        
        options = [("Home", self.init_main_menu), 
                   ("About us", self.show_about_screen), 
                   ("Contact us", self.show_contact_screen), 
                   ("Login/sign up", self.init_login_screen)]
        
        for text, command in options:
            bg = 'grey' if text == active else '#004c61'
            fg = 'white'
            tk.Button(frame, text=text, command=command, bg=bg, fg=fg, font=("Helvetica", 16, "bold"), bd=0, activebackground='black', activeforeground='white').pack(side='left', padx=10, pady=10)
        
        if self.current_account:
            tk.Label(frame, text=f"Username: {self.current_account.name}", font=("Helvetica", 16, "bold"), bg='#004c61', fg='white').pack(side='right', padx=10)
            tk.Label(frame, text=f"Balance: ${self.current_account.get_balance():.2f}", font=("Helvetica", 16, "bold"), bg='#004c61', fg='white').pack(side='right', padx=10)
    

    def update_user_info(self):
        if self.current_account:
            self.user_info_label.config(text=f"Username: {self.current_account.name}\nBalance: ${self.current_account.get_balance():.2f}")
        else:
            self.user_info_label.config(text="")

    def init_login_screen(self):
        self.clear_screen()
        self.create_navigation_bar('Login/sign up')
        
        tk.Label(self.master, text="Login / Sign Up", font=("Helvetica", 25, "bold")).pack(pady=20)

        entry_width = 30
        tk.Label(self.master, text="Username:", font=("Helvetica", 7, "bold")).pack(pady=5)
        self.username_entry = tk.Entry(self.master, font=("Helvetica", 8), width=entry_width)
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Password:", font=("Helvetica", 7, "bold")).pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*", font=("Helvetica", 8), width=entry_width)
        self.password_entry.pack(pady=5)

        tk.Button(self.master, text='Login', command=self.login, font=("Helvetica", 7, "bold")).pack(pady=5)
        self.create_account_button = tk.Button(self.master, text='Create Account', command=self.show_create_account_fields, font=("Helvetica", 8, "bold"))
        self.create_account_button.pack(pady=5)

        self.back_button = tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 12, "bold"))
        self.back_button.pack(pady=20)

        self.new_name_label = tk.Label(self.master, text="New Account Name:", font=("Helvetica", 7, "bold"))
        self.new_name_entry = tk.Entry(self.master, font=("Helvetica", 8))
        self.new_deposit_label = tk.Label(self.master, text="Initial Deposit:", font=("Helvetica", 7, "bold"))
        self.new_deposit_entry = tk.Entry(self.master, font=("Helvetica", 8))
        self.new_password_label = tk.Label(self.master, text="New Password:", font=("Helvetica", 7, "bold"))
        self.new_password_entry = tk.Entry(self.master, show="*", font=("Helvetica", 8))
        self.confirm_account_button = tk.Button(self.master, text='Confirm Account', command=self.create_account, font=("Helvetica", 12, "bold"))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        account = df_accounts[(df_accounts['username'] == username) & (df_accounts['password'] == password)]
        if not account.empty:
            transactions = account.iloc[0]['transactions']
            transactions_list = transactions.split(',') if pd.notna(transactions) else []
            self.current_account = BankAccount(username, account.iloc[0]['balance'], transactions_list)
            self.init_main_menu()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def show_create_account_fields(self):
        self.new_name_label.pack(pady=5)
        self.new_name_entry.pack(pady=5)
        self.new_deposit_label.pack(pady=5)
        self.new_deposit_entry.pack(pady=5)
        self.new_password_label.pack(pady=5)
        self.new_password_entry.pack(pady=5)
        self.confirm_account_button.pack(pady=5)

    def create_account(self):
        global df_accounts
        new_username = self.new_name_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        try:
            initial_deposit = float(self.new_deposit_entry.get().strip())
            if initial_deposit < 0:
                raise ValueError("Initial deposit must be non-negative.")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        if not new_username or not new_password:
            messagebox.showerror("Invalid input", "Username and password cannot be empty.")
            return

        if df_accounts[df_accounts['username'] == new_username].empty:
            new_account = {'username': new_username, 'password': new_password, 'balance': initial_deposit, 'transactions': f"Initial deposit: ${initial_deposit:.2f}"}
            df_accounts = pd.concat([df_accounts, pd.DataFrame([new_account])], ignore_index=True)
            df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)
            messagebox.showinfo("Account Created", f"Account created for {new_username} with initial balance of ${initial_deposit:.2f}")
            self.hide_create_account_fields()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def hide_create_account_fields(self):
        self.new_name_label.pack_forget()
        self.new_name_entry.pack_forget()
        self.new_deposit_label.pack_forget()
        self.new_deposit_entry.pack_forget()
        self.new_password_label.pack_forget()
        self.new_password_entry.pack_forget()
        self.confirm_account_button.pack_forget()

    def show_main_menu(self):
        self.init_main_menu()

    def show_withdraw_screen(self):
        self.clear_screen()
        self.create_navigation_bar(None)
        
        tk.Label(self.master, text="Withdraw Money", font=("Helvetica", 25, "bold")).pack(pady=20)

        tk.Label(self.master, text="Amount:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.amount_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.amount_entry.pack(pady=5)

        tk.Button(self.master, text='Withdraw', command=self.withdraw, font=("Helvetica", 16, "bold")).pack(pady=5)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        
        result = self.current_account.withdraw(amount)
        messagebox.showinfo("Withdraw", result)
        self.update_account_info()

    def show_deposit_screen(self):
        self.clear_screen()
        self.create_navigation_bar(None)
        
        tk.Label(self.master, text="Deposit Money", font=("Helvetica", 25, "bold")).pack(pady=20)

        tk.Label(self.master, text="Amount:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.amount_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.amount_entry.pack(pady=5)

        tk.Button(self.master, text='Deposit', command=self.deposit, font=("Helvetica", 16, "bold")).pack(pady=5)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def deposit(self):
        try:
            amount = float(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        
        result = self.current_account.deposit(amount)
        messagebox.showinfo("Deposit", result)
        self.update_account_info()

    def show_loan_screen(self):
        self.clear_screen()
        self.create_navigation_bar(None)
        
        tk.Label(self.master, text="Apply For Loan", font=("Helvetica", 25, "bold")).pack(pady=20)
        
        tk.Label(self.master, text="Loan Amount:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.loan_amount_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.loan_amount_entry.pack(pady=5)
        
        tk.Label(self.master, text="Loan Purpose:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.loan_purpose_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.loan_purpose_entry.pack(pady=5)
        
        tk.Button(self.master, text='Apply', command=self.apply_for_loan, font=("Helvetica", 16, "bold")).pack(pady=5)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def apply_for_loan(self):

        loan_amount = self.loan_amount_entry.get().strip()
        loan_purpose = self.loan_purpose_entry.get().strip()
        
        if loan_amount and loan_purpose:
            messagebox.showinfo("Loan Application", f"Loan application submitted for ${loan_amount} for {loan_purpose}.")
            self.init_main_menu()
        else:
            messagebox.showerror("Invalid input", "All fields are required.")

    def show_loan_management_screen(self):
     self.clear_screen()
     self.create_navigation_bar(None)
    
     tk.Label(self.master, text="Loan Management", font=("Helvetica", 25, "bold")).pack(pady=20)
    #seems to be the problem
     tk.Label(self.master, text=f"Loan Balance: ${self.current_account.loan_balance:.2f}", font=("Helvetica", 16, "bold")).pack(pady=10)
     tk.Label(self.master, text=f"Years to Repay: {self.current_account.years_to_repay}", font=("Helvetica", 16, "bold")).pack(pady=10)
    
     tk.Label(self.master, text="Repay Amount:", font=("Helvetica", 12, "bold")).pack(pady=5)
     self.repay_amount_entry = tk.Entry(self.master, font=("Helvetica", 12))
     self.repay_amount_entry.pack(pady=5)
    
     tk.Button(self.master, text='Repay Loan', command=self.repay_loan, font=("Helvetica", 16, "bold")).pack(pady=10)
     tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def repay_loan(self):
      try:
         repay_amount = float(self.repay_amount_entry.get().strip())
         if repay_amount <= 0:
             raise ValueError("Amount must be positive.")
      except ValueError as e:
         messagebox.showerror("Invalid input", str(e))
         return
    
      if repay_amount > self.current_account.loan_balance:
          repay_amount = self.current_account.loan_balance
    
      self.current_account.loan_balance -= repay_amount
      self.current_account.transactions.append(f"Repaid ${repay_amount:.2f} towards loan.")
      self.update_account_info()
    
      messagebox.showinfo("Loan Repayment", f"Repaid ${repay_amount:.2f}. Loan balance is now ${self.current_account.loan_balance:.2f}.")
    
      if self.current_account.loan_balance == 0:
         messagebox.showinfo("Loan Paid Off", "Congratulations! Your loan has been fully repaid.")
    
    def update_account_info(self):
     global df_accounts
     df_accounts.loc[df_accounts['username'] == self.current_account.name, 'balance'] = self.current_account.get_balance()
     df_accounts.loc[df_accounts['username'] == self.current_account.name, 'transactions'] = ','.join(self.current_account.transactions)
     df_accounts.loc[df_accounts['username'] == self.current_account.name, 'loan_balance'] = self.current_account.loan_balance
     df_accounts.loc[df_accounts['username'] == self.current_account.name, 'years_to_repay'] = self.current_account.years_to_repay
     df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)

    def show_transaction_history(self):
        self.clear_screen()
        self.create_navigation_bar(None)
        
        tk.Label(self.master, text="Transaction History", font=("Helvetica", 25, "bold")).pack(pady=20)
        
        transactions = "\n".join(self.current_account.transactions)
        tk.Label(self.master, text=transactions, font=("Helvetica", 12), justify="left").pack(pady=10)
        
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def show_account_management(self):
        self.clear_screen()
        self.create_navigation_bar(None)
        
        tk.Label(self.master, text="Account Management", font=("Helvetica", 25, "bold")).pack(pady=20)

        tk.Label(self.master, text="Change Password:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.new_password_entry = tk.Entry(self.master, show="*", font=("Helvetica", 12))
        self.new_password_entry.pack(pady=5)
        
        tk.Button(self.master, text='Change Password', command=self.change_password, font=("Helvetica", 16, "bold")).pack(pady=5)
        
        tk.Button(self.master, text='Close Account', command=self.close_account, font=("Helvetica", 16, "bold"), fg='red').pack(pady=20)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def change_password(self):
        global df_accounts
        new_password = self.new_password_entry.get().strip()
        if new_password:
            df_accounts.loc[df_accounts['username'] == self.current_account.name, 'password'] = new_password
            df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)
            messagebox.showinfo("Password Changed", "Your password has been changed successfully.")
        else:
            messagebox.showerror("Invalid input", "Password cannot be empty.")

    def close_account(self):
        global df_accounts
        answer = messagebox.askyesno("Close Account", "Are you sure you want to close your account? This action cannot be undone.")
        if answer:
            df_accounts = df_accounts[df_accounts['username'] != self.current_account.name]
            df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)
            self.current_account = None
            messagebox.showinfo("Account Closed", "Your account has been closed.")
            self.init_main_menu()

    def update_account_info(self):
        global df_accounts
        df_accounts.loc[df_accounts['username'] == self.current_account.name, 'balance'] = self.current_account.get_balance()
        df_accounts.loc[df_accounts['username'] == self.current_account.name, 'transactions'] = ','.join(self.current_account.transactions)
        df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)

    def require_login(self, func):
        def wrapper():
            if self.current_account:
                func()
            else:
                messagebox.showwarning("Login Required", "You must be logged in to perform this action.")
                self.init_login_screen()
        return wrapper

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_transfer_screen(self):
        self.clear_screen()
        self.create_navigation_bar(None)
    
        tk.Label(self.master, text="Transfer Money", font=("Helvetica", 25, "bold")).pack(pady=20)

        tk.Label(self.master, text="Recipient Username:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.recipient_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.recipient_entry.pack(pady=5)

        tk.Label(self.master, text="Amount:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.transfer_amount_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.transfer_amount_entry.pack(pady=5)
        tk.Button(self.master, text='Transfer', command=self.transfer_money, font=("Helvetica", 16, "bold")).pack(pady=5)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def transfer_money(self):
      global df_accounts
      recipient_username = self.recipient_entry.get().strip()
      try:
          amount = float(self.transfer_amount_entry.get().strip())
          if amount <= 0:
             raise ValueError("Amount must be positive.")
      except ValueError as e:
         messagebox.showerror("Invalid input", str(e))
         return

      if recipient_username == self.current_account.name:
        messagebox.showerror("Invalid input", "You cannot transfer money to yourself.")
        return

      recipient_account = df_accounts[df_accounts['username'] == recipient_username]

      if not recipient_account.empty:
         result = self.current_account.withdraw(amount)
         if "Withdrawn" in result:
            df_accounts.loc[df_accounts['username'] == recipient_username, 'balance'] += amount
            recipient_transactions = recipient_account.iloc[0]['transactions']
            recipient_transactions_list = recipient_transactions.split(',') if pd.notna(recipient_transactions) else []
            recipient_transactions_list.append(f"Received ${amount:.2f} from {self.current_account.name}")
            df_accounts.loc[df_accounts['username'] == recipient_username, 'transactions'] = ','.join(recipient_transactions_list)
            df_accounts.to_excel(EXCEL_FILE, sheet_name='accounts', index=False)
            messagebox.showinfo("Transfer Successful", f"Transferred ${amount:.2f} to {recipient_username}.")
            self.update_account_info()
         else:
            messagebox.showerror("Transfer Failed", result)
      else:
        messagebox.showerror("Transfer Failed", "Recipient username does not exist.")

    def show_about_screen(self):
        self.clear_screen()
        self.create_navigation_bar('About us')
        tk.Label(self.master, text="About us", font=("Helvetica", 30, "bold")).pack(pady=20)
        tk.Label(self.master, text="Khondokar Bank is a leading banking institution, dedicated to providing exceptional financial services.", font=("Helvetica", 17, "bold")).pack(pady=10)
        tk.Label(self.master, text="Our mission is to help you build your future by offering personalized and innovative banking solutions.", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

    def show_contact_screen(self):
        self.clear_screen()
        self.create_navigation_bar('Contact us')
        tk.Label(self.master, text="Contact us", font=("Helvetica", 30, "bold")).pack(pady=20)
        tk.Label(self.master, text="Phone: +123 456 7890", font=("Helvetica", 20)).pack(pady=10)
        tk.Label(self.master, text="Email: support@khondokarbank.com", font=("Helvetica", 20)).pack(pady=10)
        tk.Button(self.master, text='Back', command=self.init_main_menu, font=("Helvetica", 16, "bold")).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.geometry("800x600")
    root.mainloop() 
