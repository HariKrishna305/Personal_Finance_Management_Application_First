import unittest
import sqlite3
from unittest.mock import patch
from personal_finance_app import (create_connection,register_user,login_user,add_transaction,set_budget,create_user_table,create_transactions_table,create_budgets_table,)


class TestPersonalFinanceApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
 # Setup the database and tables before all tests
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS transactions")
        cursor.execute("DROP TABLE IF EXISTS budgets")
        connection.commit()
        connection.close()

# Create tables for testing
        create_user_table()
        create_transactions_table()
        create_budgets_table()

    def setUp(self):
# Ensure that the tables are empty before each test
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM budgets")
        connection.commit()
        connection.close()

    def test_user_registration(self):
        username = "testuser"
        password = "testpassword"

# Mock input for registration
        with patch("builtins.input", side_effect=[username, password]):
            register_user()

# Verify the user in the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()

        self.assertEqual(result[0], username, "User registration failed")

    def test_user_login(self):
        username = "testuser"
        password = "testpassword"

# Register the user first
        with patch("builtins.input", side_effect=[username, password]):
            register_user()

# Login with correct credentials
        with patch("builtins.input", side_effect=[username, password]):
            user_id = login_user()
        self.assertIsNotNone(user_id, "Login failed with correct credentials")

# Login with incorrect credentials
        with patch("builtins.input", side_effect=[username, "wrongpassword"]):
            wrong_user_id = login_user()
        self.assertIsNone(wrong_user_id, "Login should fail with incorrect password")

    def test_add_transaction(self):
        username = "testuser"
        password = "testpassword"

# Register and login the user
        with patch("builtins.input", side_effect=[username, password]):
            register_user()
        with patch("builtins.input", side_effect=[username, password]):
            user_id = login_user()

# Mock adding a transaction
        with patch("builtins.input", side_effect=["income", "60000", "Salary", "Salary"]):
            add_transaction(user_id)

# Verify the transaction in the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM transactions WHERE user_id = ? AND type = ? AND amount = ?",
            (user_id, "income", 60000.0),
        )
        result = cursor.fetchone()
        connection.close()

        self.assertIsNotNone(result, "Transaction addition failed")

    def test_set_budget(self):
        username = "testuser"
        password = "testpassword"

# Register and login the user
        with patch("builtins.input", side_effect=[username, password]):
            register_user()
        with patch("builtins.input", side_effect=[username, password]):
            user_id = login_user()

# Mock setting a budget
        with patch("builtins.input", side_effect=["Food", "5000", "12", "2024"]):
            set_budget(user_id)

# Verify the budget in the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM budgets WHERE user_id = ? AND category = ? AND amount = ? AND month = ? AND year = ?",
            (user_id, "Food", 5000.0, 12, 2024),
        )
        result = cursor.fetchone()
        connection.close()

        self.assertIsNotNone(result, "Budget setting failed")


if __name__ == "__main__":
    unittest.main()
