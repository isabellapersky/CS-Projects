# Isabella Persky
# Enhanced intranet system for navigating menu options and registering new users to be added to the flask app database

import csv
import hashlib
import os
import random
import re
import sqlite3
import string

csv_filename = 'users'

# Function to hash and salt password (took from my program in lab6)
# Takes a plain-text password, generates a 40-character salt, hashes the combination using SHA-1, returns the concatenated salt and hash password
def hash_password(password):
    salt = os.urandom(20).hex()
    hashable = salt + password
    hashable = hashable.encode('utf-8')  # Convert hash to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # Hash with SHA-1
    return salt + this_hash  # Returns concatenated salt and hash
    
# Function to generate a strong random password
def generate_strong_password():
    length = random.randint(8, 25)
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password
    
# Function to validate the password, checks for length, uppercase, lowercase, and special character constraints
def validate_password(password):
    if len(password) < 8 or len(password) > 25:
        return "Password must be between 8 and 25 characters long."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number."
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    return None
    
# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Allows access by column name
    return conn

# Function to load users from the database
# Reads username, password, and access level from the database and enters into a dict
def load_users_from_db():
    users = {}
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT username, password, access_level FROM users')
    rows = cursor.fetchall()
    for row in rows:
        users[row['username']] = {
            'password': row['password'],
            'access_level': row['access_level']
        }

    conn.close()
    return users

# Function to add user to the database
# Password is hashed before being inserted into database
def add_user_to_db(username, password, access_level):
    hashed_password = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the new user or update the existing user's password (had to add the update functionality because I ran into login issues with existing credentials, as I was still modiying the code for the password hash function)
        cursor.execute('''INSERT INTO users (username, password, access_level)
                          VALUES (?, ?, ?)
                          ON CONFLICT(username) DO UPDATE SET password = excluded.password''',
                       (username, hashed_password, access_level))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    
    conn.close()

# Function to load existing users from CSV and insert them into the database (needed to do this in order to initially login, otherwise would have no credentials to get into system)
def migrate_users_to_db(csv_filename):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the users table if doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        access_level TEXT NOT NULL
                    )''')
    conn.commit()

    # Open the CSV file and read user credentials
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row['username']
            password = row['password']
            access_level = row['access_level']

            # Add each user to the database
            add_user_to_db(username, password, access_level)

    conn.close()

# Function to handle user login
def login(users):
    print("Welcome to the Catamount Company Intranet System!")
    attempts = 0
    while attempts < 3:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in users:
            stored_password = users[username]['password']  # This is the full salt + hash
            salt = stored_password[:40]  # Extract the first 40 characters as the salt
            expected_hash = stored_password[40:]  # The rest is the hash

            # Hash the input password with the stored salt
            hashed_input_password = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()

            if hashed_input_password == expected_hash:
                print(f"\nLogin successful. Welcome, {username}!")
                return users[username]['access_level']
            else:
                print("Invalid username or password.\n")
        else:
            print("Invalid username or password.\n")
        # 3 attempts given for login
        attempts += 1
        print(f"{3 - attempts} attempts remaining.\n")

    print("Too many failed attempts. Please try again later.")
    return None

# Function to display the menu based on the user's access level
def display_menu(access_level):
    menu = {
        'admin': ["1. Time Reporting", "2. Accounting", "3. Register New User", "4. Exit"],
        'manager': ["1. Time Reporting", "3. Register New User", "4. Exit"],
        'employee': ["1. Time Reporting", "4. Exit"]
    }

    options = menu[access_level]

    print("\nMenu Options:")
    for option in options:
        print(option)

# Function to handle menu selection and access levels
def handle_menu_selection(access_level):
    authorized_menu = {
        'admin': ["Time Reporting", "Accounting", "Register New User"],
        'manager': ["Time Reporting", "Accounting"],
        'employee': ["Time Reporting"]
    }

    while True:
        display_menu(access_level)
        choice = input("\nSelect a menu option (enter the number): ")

        if choice == '1':
            print("You have now accessed the Time Reporting application.\n")
        elif choice == '2' and access_level in ['admin']:
            print("You have now accessed the Accounting application.\n")
        elif choice == '3' and access_level in ['admin', 'manager']:
            register_new_user()
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option or you are not authorized to access this area.\n")
            
# Function to register a new user with password validation and strong password generator option
def register_new_user():
    print("\nRegister New User")
    username = input("Enter new username: ")
    while True:
        choice = input("Would you like a password to be generated for you? (y/n): ")
        if choice.lower() == 'y':
            password = generate_strong_password()
            print(f"Generated password: {password}")
            break
        elif choice.lower() == 'n':
            password = input("Enter new password: ")
            error_message = validate_password(password)
        else:
            print("Please enter a valid choice.")
            continue
        if error_message:
            print(f"Error: {error_message}")
        else:
            break
    while True:
        # Decided to give the option to choose access level instead of defaulting to lowest level (employee)
        access_level = input("Enter access level (admin/manager/employee): ")
    
        # Checks if the access level input is not a valid option
        if access_level not in ('admin', 'manager', 'employee'):
            print("Please enter a valid choice.")
            continue  # Restart the loop if input invalid
    
        add_user_to_db(username, password, access_level)
        print(f"User {username} registered successfully!\n")
        break  # Exit loop after successful registration


# Main program
def main():
    # If the database is empty, migrate users from the CSV file
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table in users.db if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        access_level TEXT NOT NULL )''')
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        migrate_users_to_db(csv_filename)  # Inserts the users from the CSV file into the database table
    conn.close()

    # Load users from the database
    users = load_users_from_db()

    # Prompt login
    access_level = login(users)
    if access_level:
        handle_menu_selection(access_level)

if __name__ == '__main__':
    main()
