import random
import string
import os
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


# Create an instance of the Google Sheets client
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


# Open the worksheet
WORKSHEET = GSPREAD_CLIENT.open('passwords').sheet1


# Function to generate a random password
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


# Function to add a password to the worksheet
def add_password(website, username, password, user_id):
    row = [website, username, password, user_id]
    WORKSHEET.append_row(row)


# Function to get a password from the worksheet
def get_password(website, user_id):
    data = WORKSHEET.get_all_values()
    for row in data[1:]:
        if row[0] == website and row[3] == user_id:
            return row[2]
    return None


# Function for initial login
def initial_login():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    print("""

   ╔═╗┌─┐┌─┐┌─┐╔═╗┌─┐┌┐┌┬┬ ┬┌─┐
   ╠═╝├─┤└─┐└─┐║ ╦├┤ │││││ │└─┐
   ╩  ┴ ┴└─┘└─┘╚═╝└─┘┘└┘┴└─┘└─┘
""")
    print("\n" * 4)
    print("   Welcome! Please select an option:")
    print()
    print("     1. Login")
    print("     2. Create new user")
    print("     3. Quit")
    print()
    choice = input("   Enter your choice: ")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    if choice == "1":
        username = input("   Enter your username: ")
        password = input("   Enter your password: ")
        data = WORKSHEET.get_all_values()
        for row in data[1:]:
            if row[1] == username and row[2] == password:
                user_id = row[3]
                os.system('cls' if os.name == 'nt' else 'clear')
                print("   Welcome, {}!".format(username))
                menu(user_id)   # Pass the user ID to the menu function
                break
        else:
            print("   Incorrect username or password.")
            input("   Press Enter to continue...")
            initial_login()
    elif choice == "2":
        username = input("   Enter a new username: ")
        password = input("   Enter a new password: ")
        print()
        data = WORKSHEET.get_all_values()
        user_id = str(len(data))
        row = [user_id, username, password, user_id]
        WORKSHEET.append_row(row)
        print("   New user created. Please log in.")
        input("   Press Enter to continue...")
        initial_login()
    elif choice == "3":
        print("   Goodbye!")
        quit()
    else:
        print("   Invalid choice, try again.")
        initial_login()


# Menu function
def menu(user_id):
    print("     1. Generate a password for a new website")
    print("     2. Get a password for an existing website")
    print("     3. Quit")
    print()
    choice = input("   Enter your choice: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    if choice == "1":
        website = input("   Enter the website: ")
        username = input("   Enter the username: ")
        password = generate_password()
        print()
        print("   Generated password:", password)
        print()
        add_password(website, username, password, user_id)
        # Pass the user ID to the add_password function
    elif choice == "2":
        website = input("   Enter the website: ")
        password = get_password(website, user_id)
        # Pass the user ID to the get_password function
        if password:
            print("   Password:", password)
        else:
            print("   No password found for", website)
    elif choice == "3":
        print("   Goodbye!")
        quit()
    else:
        print("   Invalid choice, try again.")
    menu(user_id)


# 1Start the program
initial_login()
