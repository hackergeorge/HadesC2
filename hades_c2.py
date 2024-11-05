import bcrypt
import getpass
import os

# ASCII Art Skull
SKULL_ART = """
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⠴⠶⠶⠶⠶⠶⠶⠶⠶⢤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⠶⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠶⣤⡀⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⡄⠀⠀⠀
⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣦⠀⠀
⢰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⠀
⣿⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡄⠀⢹⡄
⡏⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢸⡇
⣿⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⢸⡇
⢹⡆⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⣾⠀
⠈⢷⡀⢸⡇⠀⢀⣠⣤⣶⣶⣶⣤⡀⠀⠀⠀⠀⠀⢀⣠⣶⣶⣶⣶⣤⣄⠀⠀⣿⠀⣼⠃⠀
⠀⠈⢷⣼⠃⠀⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⡾⠃⠀⠀
⠀⠀⠈⣿⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⠃⠀⢸⡇⠀⠀⠀
⠀⠀⠀⣿⠀⠀⠘⢿⣿⣿⣿⣿⡿⠃⠀⢠⠀⣄⠀⠀⠙⢿⣿⣿⣿⡿⠏⠀⠀⢘⡇⠀⠀⠀
⠀⠀⠀⢻⡄⠀⠀⠀⠈⠉⠉⠀⠀⠀⣴⣿⠀⣿⣷⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⢸⡇⠀⠀⠀
⠀⠀⠀⠈⠻⣄⡀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠀⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣟⠳⣦⡀⠀⠀⠀⠸⣿⡿⠀⢻⣿⡟⠀⠀⠀⠀⣤⡾⢻⡏⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡄⢻⠻⣆⠀⠀⠀⠈⠀⠀⠀⠈⠀⠀⠀⢀⡾⢻⠁⢸⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡇⠀⡆⢹⠒⡦⢤⠤⡤⢤⢤⡤⣤⠤⡔⡿⢁⡇⠀⡿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡇⠀⢣⢸⠦⣧⣼⣀⡇⢸⢀⣇⣸⣠⡷⢇⢸⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣷⠀⠈⠺⣄⣇⢸⠉⡏⢹⠉⡏⢹⢀⣧⠾⠋⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠻⣆⠀⠀⠀⠈⠉⠙⠓⠚⠚⠋⠉⠁⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⠶⠦⣤⣤⣤⡤⠶⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# Dictionary to store user details and logs
users_db = {}
logs = {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_skull():
    clear_screen()
    print(SKULL_ART)

def encrypt_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(stored_password, entered_password):
    return bcrypt.checkpw(entered_password.encode(), stored_password)

def create_admin():
    display_skull()
    print("Welcome To HADES Warshipping Device Interface.")
    print("Let's create your admin account:\n")
    name = input("Enter your name: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    verify_pass = getpass.getpass("Verify your password: ")
    
    if password != verify_pass:
        print("Passwords did not match. Womp womp.")
        return create_admin()
    
    users_db[username] = {
        'name': name,
        'password': encrypt_password(password),
        'is_admin': True
    }
    logs[username] = []
    print("Admin account created successfully! Returning to login page...\n")
    login()  # After creating admin, go to login

def admin_menu():
    while True:
        display_skull()
        print("1. Create New User")
        print("2. Edit Existing User")
        print("3. View Logs")
        print("4. Logout")
        choice = input("Choose an option: ")
        
        if choice == '1':
            create_user()
        elif choice == '2':
            edit_user()
        elif choice == '3':
            view_logs()
        elif choice == '4':
            login()  # Logout and return to login page
        else:
            print("Invalid option.")

def create_user():
    display_skull()
    username = input("Enter new user's username: ")
    temp_password = getpass.getpass("Enter temporary password: ")
    users_db[username] = {
        'password': encrypt_password(temp_password),
        'is_admin': False
    }
    logs[username] = []
    print(f"User {username} created with a temporary password.")

def edit_user():
    display_skull()
    print("Active users:")
    for i, user in enumerate(users_db.keys(), 1):
        print(f"{i}. {user}")
    
    choice = int(input("Select a user to edit: ")) - 1
    user = list(users_db.keys())[choice]
    new_temp_password = getpass.getpass(f"Enter a new temporary password for {user}: ")
    users_db[user]['password'] = encrypt_password(new_temp_password)
    print(f"Temporary password for {user} updated.")

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

def user_menu():
    while True:
        display_skull()
        print("Welcome To The C2 Command Center.\n")
        print("1. Select a device")
        print("2. Verify System Health")
        print("3. Exit Application")
        choice = input("Choose an option: ")
        
        if choice == '1':
            print("Device selection feature coming soon.")
        elif choice == '2':
            print("System health verification feature coming soon.")
        elif choice == '3':
            login()  # Logout and return to login page
            break
        else:
            print("Invalid option.")

def login():
    display_skull()
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    
    if username in users_db and verify_password(users_db[username]['password'], password):
        if users_db[username]['is_admin']:
            admin_menu()
        else:
            user_menu()
    else:
        print("Invalid username or password.")
        login()

# Main Execution
if not users_db:
    create_admin()
else:
    login()
