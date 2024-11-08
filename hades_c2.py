import bcrypt
import getpass
import os
import json
import time
import re

SKULL_ART = """ 
\033[31m   ██░ ██  ▄▄▄      ▓█████▄ ▓█████   ██████ 
\033[31m  ▓██░ ██▒▒████▄    ▒██▀ ██▌▓█   ▀ ▒██    ▒ 
\033[31m  ▒██▀▀██░▒██  ▀█▄  ░██   █▌▒███   ░ ▓██▄   
\033[31m  ░▓█ ░██ ░██▄▄▄▄██ ░▓█▄   ▌▒▓█  ▄   ▒   ██▒
\033[31m  ░▓█▒░██▓ ▓█   ▓██▒░▒████▓ ░▒████▒▒██████▒▒
\033[31m   ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▒▓  ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░
\033[31m   ░░▒░ ░  ▒   ▒▒ ░ ░ ▒  ▒  ░ ░  ░░ ░▒  ░ ░
\033[0m   ░  ░░ ░  ░   ▒    ░ ░  ░    ░   ░  ░  ░  
                    ░                      """

# File to store data
DATA_FILE = "data.json"  # Adjust path if necessary

# Dictionary to store user details and logs
users_db = {}
logs = {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_skull():
    clear_screen()
    print(SKULL_ART)

def encrypt_password(password):
    """Hash the password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(stored_password, entered_password):
    """Verify the password by comparing bcrypt hashes."""
    return bcrypt.checkpw(entered_password.encode(), stored_password)

def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting...")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def log_action(user, action):
    """Log actions performed by users."""
    logs[user].append(f"{time.ctime()}: {action}")
    save_data(users_db, logs)

def validate_password(password):
    """Validate the password based on required criteria."""
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not re.search(r"[A-Z]", password):  # At least one uppercase letter
        print("Password must contain at least one uppercase letter.")
        return False
    if not re.search(r"[a-z]", password):  # At least one lowercase letter
        print("Password must contain at least one lowercase letter.")
        return False
    if not re.search(r"[0-9]", password):  # At least one number
        print("Password must contain at least one number.")
        return False
    if not re.search(r"[@$!%*?&]", password):  # At least one special character
        print("Password must contain at least one special character.")
        return False
    return True

def create_admin():
    while True:
        display_skull()
        print("Create Your Admin Account:\n")
        name = input("Enter your name: ")
        username = input("Enter your pseudonym: ")
        password = getpass.getpass("Enter your password: ")

        # Validate the password
        if not validate_password(password):
            continue  # Skip to next iteration if validation fails

        verify_pass = getpass.getpass("Verify your password: ")

        if password != verify_pass:
            print("Passwords did not match. Try again.")
            continue

        hashed_password = encrypt_password(password)
        users_db[username] = {
            'name': name,
            'password': hashed_password,
            'is_admin': True
        }
        logs[username] = []
        print("Admin account created successfully!")
        log_action(username, "Admin account created.")
        save_data(users_db, logs)
        login()
        break

def admin_menu():
    while True:
        display_skull()
        print("1. Create New User")
        print("2. Edit Existing User")
        print("3. View Logs")
        print("4. Logout")
        choice = safe_input("Choose an option: ")

        if choice == '1':
            create_user()
        elif choice == '2':
            edit_user()
        elif choice == '3':
            view_logs()
        elif choice == '4':
            print("Logging out...")
            log_action(current_user, "Logged out from admin menu.")
            break  # Exit admin menu
        else:
            print("Invalid option. Please try again.")
            time.sleep(2)

    login()  # After breaking the loop, return to login

def create_user():
    display_skull()
    username = input("Enter new user's username: ")
    temp_password = getpass.getpass("Enter temporary password: ")

    # Validate the password
    if not validate_password(temp_password):
        return  # If password is invalid, exit the function

    verify_pass = getpass.getpass("Verify the temporary password: ")
    if temp_password != verify_pass:
        print("Passwords did not match. Try again.")
        return

    # Hash the temporary password
    hashed_password = encrypt_password(temp_password)
    users_db[username] = {
        'password': hashed_password,
        'is_admin': False
    }
    logs[username] = []
    print(f"User {username} created with a temporary password.")
    log_action(current_user, f"Created new user {username}.")
    save_data(users_db, logs)

def edit_user():
    display_skull()
    print("Active users:")
    for i, user in enumerate(users_db.keys(), 1):
        print(f"{i}. {user}")
    
    choice = int(input("Select a user to edit: ")) - 1
    user = list(users_db.keys())[choice]
    new_temp_password = getpass.getpass(f"Enter a new temporary password for {user}: ")
    
    # Validate the new temporary password
    if not validate_password(new_temp_password):
        return  # If password is invalid, exit the function

    # Hash the new temporary password
    hashed_password = encrypt_password(new_temp_password)
    users_db[user]['password'] = hashed_password
    print(f"Temporary password for {user} updated.")
    log_action(current_user, f"Updated temporary password for {user}.")
    save_data(users_db, logs)

def view_logs():
    display_skull()
    print("Users:")
    for i, user in enumerate(users_db.keys(), 1):
        print(f"{i}. {user}")
    
    choice = int(input("Select a user to view logs: ")) - 1
    user = list(users_db.keys())[choice]
    print(f"Logs for {user}:")
    for log in logs[user]:
        print(log)
    input("Press Enter to continue...")

def user_menu():
    while True:
        display_skull()
        print("Welcome to the HADES C2 Command Center.")
        print("1. Select A Device")
        print("2. Add New Device")
        print("3. Verify System Health")
        print("4. Exit Application")
        choice = safe_input("Choose an option: ")

        if choice == '1':
            print("Device selection feature coming soon.")
            time.sleep(3)
        elif choice == '2':
            print("System health verification feature coming soon.")
            time.sleep(3)
        elif choice == '3': 
            print("New Device connection coming soon.")
            time.sleep(3)
        elif choice == '4':
            print("Logging out...")
            log_action(current_user, "Logged out from user menu.")
            break  # Exit user menu
        else:
            print("Invalid option. Please try again.")
            time.sleep(3)

    login()  # After breaking the loop, return to login

def login():
    global current_user
    try:
        display_skull()
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        if username in users_db and verify_password(users_db[username]['password'], password):
            current_user = username  # Set the current user
            log_action(current_user, "Logged in.")
            if users_db[username]['is_admin']:
                admin_menu()
            else:
                user_menu()
        else:
            print("Login failed.")
            input("Press Enter to continue...")
            login()

    except KeyboardInterrupt:
        print("\nSee Ya You Are Now Exiting...")
        exit()

def load_data():
    if not os.path.exists(DATA_FILE):
        print("Data file not found. Creating a new one.")
        return {}, {}

    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            if not data:
                return {}, {}
            return data.get("users_db", {}), data.get("logs", {})
    except json.JSONDecodeError as e:
        print(f"Error reading {DATA_FILE}: {e}")
        print("Reinitializing data...")
        return {}, {}

def save_data(users_db, logs):
    data = {"users_db": users_db, "logs": logs}
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    users_db, logs = load_data()
    login()
