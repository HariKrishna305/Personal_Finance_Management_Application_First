import sqlite3
# Connect to SQLite database

def create_connection():
    connection = sqlite3.connect('Finance_app.db')
    return connection

# Create Users table
def create_user_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password TEXT)''')
    connection.commit()
    connection.close()

# Create Transactions table
def create_transactions_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,type TEXT,amount REAL,description TEXT,category TEXT,date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES users(id))''')
    connection.commit()
    connection.close()

# Create Budgets table
def create_budgets_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,category TEXT,amount REAL,month INTEGER,year INTEGER,FOREIGN KEY (user_id) REFERENCES users(id))''')
    connection.commit()
    connection.close()

# Backup database
import shutil

def backup_database():
    try:
        backup_file = 'finance_app_backup.db'
        shutil.copy('Finance_app.db', backup_file)
        print(f"Backup created successfully! Backup file: {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")

# Restore database
import os
def restore_database():
    try:
        backup_file = 'finance_app_backup.db'
        if os.path.exists(backup_file):
            shutil.copy(backup_file, 'Finance_app.db')
            print("Database restored successfully!")
        else:
            print("Backup file not found.")
    except Exception as e:
        print(f"Error restoring database: {e}")

# Register user
def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hashed_password))
        connection.commit()
        print("Registration successful!")
        connection.close()
    except sqlite3.IntegrityError:
        print("Username already exists.")
    except Exception as e:
        print(f"Error: {e}")

# Login user
import bcrypt

def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()
    if result:
        user_id, stored_password_hash = result
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            print("Login successful!")
            return user_id
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")
    return None

# Add transaction
def add_transaction(user_id):
    transaction_type = input("Enter transaction type (income/expense): ").lower()
    amount = float(input("Enter the amount: "))
    description = input("Enter a description: ")
    category = input("Enter category: ")
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, amount, description, category) VALUES (?, ?, ?, ?, ?)",
                   (user_id, transaction_type, amount, description, category))
    connection.commit()
    print("Transaction added successfully!")
    connection.close()

# Update transaction
def update_transaction(user_id):
    transaction_id = int(input("Enter the transaction ID to update: "))
    new_amount = float(input("Enter the new amount: "))
    new_description = input("Enter the new description: ")
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE transactions SET amount = ?, description = ? WHERE id = ? AND user_id = ?",
                   (new_amount, new_description, transaction_id, user_id))
    connection.commit()
    print("Transaction updated successfully!")
    connection.close()

# Delete transaction
def delete_transaction(user_id):
    transaction_id = int(input("Enter the transaction ID to delete: "))
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
    connection.commit()
    print("Transaction deleted successfully!")
    connection.close()

# List transactions
def list_transactions(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()
    print("\nTransactions:")
    for transaction in transactions:
        print(transaction)
    connection.close()

# Generate report
def generate_report(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type", (user_id,))
    report = cursor.fetchall()
    print("\nReport:")
    for entry in report:
        print(f"{entry[0].capitalize()}: ${entry[1]:.2f}")
    connection.close()


# Set budget
from datetime import datetime

def set_budget(user_id):
    try:
        category = input("Enter the category for the budget: ")
        amount = float(input("Enter the budget amount: "))
        month = int(input("Enter the month (1-12): "))
        year = int(input("Enter the year: "))

        connection = create_connection()
        cursor = connection.cursor()

        # Check if a budget already exists for the category, month, and year
        cursor.execute(
            '''SELECT id FROM budgets WHERE user_id = ? AND category = ? AND month = ? AND year = ?''',
            (user_id, category, month, year),
        )
        result = cursor.fetchone()

        if result:
            # Update existing budget
            budget_id = result[0]
            cursor.execute(
                '''UPDATE budgets SET amount = ? WHERE id = ?''',
                (amount, budget_id),
            )
            print(f"Budget for {category} updated to ${amount:.2f}.")
        else:
            # Insert new budget
            cursor.execute(
                '''INSERT INTO budgets (user_id, category, amount, month, year) VALUES (?, ?, ?, ?, ?)''',
                (user_id, category, amount, month, year),
            )
            print(f"Budget for {category} set to ${amount:.2f}.")
        
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error setting budget: {e}")

# Main application
def main():
    create_user_table()
    create_transactions_table()
    create_budgets_table()

    user_id = None
    while True:
        print("\nPersonal Finance Management Application")
        print("1. Register")
        print("2. Login")
        print("3. Add Transaction")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. List Transactions")
        print("7. Generate Report")
        print("8. Set Budget")
        print("9. Backup Data")
        print("10. Restore Data")
        print("11. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            user_id = login_user()
        elif choice == '3':
            if user_id:
                add_transaction(user_id)
            else:
                print("Please login first.")
        elif choice == '4':
            if user_id:
                update_transaction(user_id)
            else:
                print("Please login first.")
        elif choice == '5':
            if user_id:
                delete_transaction(user_id)
            else:
                print("Please login first.")
        elif choice == '6':
            if user_id:
                list_transactions(user_id)
            else:
                print("Please login first.")
        elif choice == '7':
            if user_id:
                generate_report(user_id)
            else:
                print("Please login first.")
        elif choice == '8':
            if user_id:
                set_budget(user_id)
            else:
                print("Please login first.")
        elif choice == '9':
            backup_database()
        elif choice == '10':
            restore_database()
        elif choice == '11':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
