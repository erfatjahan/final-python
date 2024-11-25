class Account:
    account_number_generator = 1001

    def __init__(self, name, email, address, account_type):
        self.account_number = Account.account_number_generator
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transaction_history = []
        self.loan_count = 0
        Account.account_number_generator += 1

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: {amount}")
            print(f"Deposit successful! New balance: {self.balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount, bank):
        if amount > bank.get_bank_total_balance():
            print("The bank is bankrupt.")
        elif amount > self.balance:
            print("Amount exceeds your account balance.")
        elif amount > 0:
            self.balance -= amount
            bank.total_loans -= amount 
            self.transaction_history.append(f"Withdrew: {amount}")
            print(f"Withdrawal successful! New balance: {self.balance}")
        else:
            print("Invalid withdrawal amount.")

    def transfer(self, amount, recipient, bank):
        if amount > bank.get_bank_total_balance():
            print("Transfer failed: The bank is bankrupt.")
        elif amount > self.balance:
            print("Transfer failed: Insufficient balance in your account.")
        elif amount > 0:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append(f"Transferred: {amount} to Account {recipient.account_number}")
            recipient.transaction_history.append(f"Received: {amount} from Account {self.account_number}")
            print(f"Transfer successful! New balance: {self.balance}")
        else:
            print("Invalid transfer amount.")

    def take_loan(self, amount, loan_enabled):
        if not loan_enabled:
            print("Loan feature is disabled.")
        elif self.loan_count >= 2:
            print("Loan limit reached. Maximum of 2 loans allowed.")
        elif amount > 0:
            self.balance += amount
            self.loan_count += 1
            bank.total_loans+=amount
            self.transaction_history.append(f"Loan taken: {amount}")
            print(f"Loan approved! New balance: {self.balance}")
        else:
            print("Invalid loan amount.")

    def view_transaction_history(self):
        if not self.transaction_history:
            print("No transactions found.")
        else:
            print("Transaction History:")
            for transaction in self.transaction_history:
                print(transaction)

    def check_balance(self):
        print(f"Available Balance: {self.balance}")


class Bank:
    def __init__(self):
        self.accounts = []
        self.total_loans = 0
        self.loan_enabled = True
        self.admin_id = "admin"
        self.admin_password = "1234"

    def create_account(self, name, email, address, account_type):
        account = Account(name, email, address, account_type)
        self.accounts.append(account)
        print(f"Account created successfully! Account Number: {account.account_number}")
        return account

    def delete_account(self, account_number):
        account = self.find_account_by_number(account_number)
        if account:
            self.accounts.remove(account)
            print(f"Account {account_number} deleted successfully.")
        else:
            print(f"Account {account_number} not found.")

    def find_account_by_number(self, account_number):
        return next((acc for acc in self.accounts if acc.account_number == account_number), None)

    def view_all_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            print("All Accounts:")
            for account in self.accounts:
                print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}, Loans Taken: {account.loan_count}")

    def check_total_balance(self):
        total_balance = sum(account.balance for account in self.accounts)
        print(f"Total Balance in Bank: {total_balance}")

    def check_total_loans(self):
        print(f"Total Loan Amount: {self.total_loans}")

    def toggle_loan_feature(self, status):
        self.loan_enabled = status
        print(f"Loan feature {'enabled' if status else 'disabled'}.")

    def get_bank_total_balance(self):
        return sum(account.balance for account in self.accounts)
bank = Bank()

def admin_menu():
    while True:
        print("\n*** ADMIN MENU ***")
        print("1. Create User Account")
        print("2. Delete User Account")
        print("3. View All Accounts")
        print("4. Check Total Balance")
        print("5. Check Total Loans")
        print("6. Toggle Loan Feature")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            account_type = input("Enter account type (Savings/Current): ")
            bank.create_account(name, email, address, account_type)
        elif choice == "2":
            acc_num = int(input("Enter account number to delete: "))
            bank.delete_account(acc_num)
        elif choice == "3":
            bank.view_all_accounts()
        elif choice == "4":
            bank.check_total_balance()
        elif choice == "5":
            bank.check_total_loans()
        elif choice == "6":
            status = input("Enable loans? (yes/no): ").strip().lower() == "yes"
            bank.toggle_loan_feature(status)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")

def user_menu():
    while True:
        print("\n*** USER MENU ***")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Take Loan")
        print("6. View Balance")
        print("7. View Transaction History")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type (Savings/Current): ").strip().capitalize()
            if account_type in ["Savings", "Current"]:
                account = bank.create_account(name, email, address, account_type)
                print("\nAccount created successfully!")
                print(f"Account Number: {account.account_number}")
                print(f"Name: {account.name}")
                print(f"Email: {account.email}")
                print(f"Address: {account.address}")
                print(f"Account Type: {account.account_type}")
                print(f"Balance: {account.balance}")
            else:
                print("Invalid account type. Please enter either 'Savings' or 'Current'.")
        elif choice == "2":
            acc_num = int(input("Enter your account number: "))
            account = bank.find_account_by_number(acc_num)
            if account:
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
            else:
                print("Account not found.")
        elif choice == "3":
            acc_num = int(input("Enter your account number: "))
            account = bank.find_account_by_number(acc_num)
            if account:
                amount = float(input("Enter amount to withdraw: "))
                account.withdraw(amount, bank)
            else:
                print("Account not found.")
        elif choice == "4":
            sender_num = int(input("Enter your account number: "))
            recipient_num = int(input("Enter recipient's account number: "))
            amount = float(input("Enter amount to transfer: "))
            sender = bank.find_account_by_number(sender_num)
            recipient = bank.find_account_by_number(recipient_num)
            if sender and recipient:
                sender.transfer(amount, recipient, bank)
            else:
                print("Account not found.")
        elif choice == "5":
            acc_num = int(input("Enter your account number: "))
            account = bank.find_account_by_number(acc_num)
            if account:
                amount = float(input("Enter loan amount: "))
                account.take_loan(amount, bank.loan_enabled)
            else:
                print("Account not found.")
        elif choice == "6":
            acc_num = int(input("Enter your account number: "))
            account = bank.find_account_by_number(acc_num)
            if account:
                account.check_balance()
            else:
                print("Account not found.")
        elif choice == "7":
            acc_num = int(input("Enter your account number: "))
            account = bank.find_account_by_number(acc_num)
            if account:
                account.view_transaction_history()
            else:
                print("Account not found.")
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")

def main():
    while True:
        print("\n*** MAIN MENU ***")
        print("1. Admin Login")
        print("2. User Access")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            admin_id = input("Enter admin ID: ")
            admin_pass = input("Enter admin password: ")
            if admin_id == bank.admin_id and admin_pass == bank.admin_password:
                admin_menu()
            else:
                print("Invalid admin.")
        elif choice == "2":
            user_menu()
        elif choice == "3":
            print("THANK YOU!")
            break
        else:
            print("Invalid choice.Please try again.")
main()
