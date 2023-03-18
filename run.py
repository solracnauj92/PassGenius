import random
import string
import gspread
from google.oauth2.service_account import Credentials
import os

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