import sqlite3
import os
import hashlib

# Database file path
USER_DB_PATH = './secure_db/user_db.sqlite3'

def hash_password(password):
    """Returns a hashed version of the given password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_db():
    """Creates the user database for storing all user-related data."""
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()

    # Create table for storing user credentials and info
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def add_user(phone_number, first_name, last_name, username, password):
    """Add a new user with their information and credentials."""
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()

    # Hash the password (no salting, as per the updated approach)
    hashed_password = hash_password(password)

    # Insert the user with all details, including hashed password
    cursor.execute('''
    INSERT INTO user_credentials (phone_number, first_name, last_name, username, password)
    VALUES (?, ?, ?, ?, ?)
    ''', (phone_number, first_name, last_name, username, hashed_password))

    conn.commit()
    conn.close()

def setup_database():
    """Main function to set up the database."""
    os.makedirs('./secure_db', exist_ok=True)  # Create the directory if it doesn't exist
    create_user_db()
    print("Database set up successfully.")

if __name__ == '__main__':
    setup_database()

    # Add a test user to the database (for testing purposes)
    add_user('1234567890', 'YourFirstName', 'YourLastName', 'yourusername', 'yourpassword')  # Replace with your data

    print("Test user added to the database.")
