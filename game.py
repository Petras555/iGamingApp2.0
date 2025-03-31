from classes import Client
from database import db_query, connection
import datetime


def username_check():
    all_usernames_db = "SELECT Username FROM Clients"
    all_usernames = []

    for x in db_query(connection, all_usernames_db):
        y = x[0]
        all_usernames.append(y)
    return all_usernames


def password_check(username):
    password_in_db = None
    password_search = f"SELECT * FROM Clients WHERE Username = '{username}'"
    for i in db_query(connection, password_search):
        password_in_db = i[2]
    return password_in_db


def create_account():
    client_id = 1

    all_client_ids_db = "SELECT ClientID FROM Clients"
    all_client_ids = []

    for x in db_query(connection, all_client_ids_db):
        y = x[0]
        all_client_ids.append(y)

    while client_id in all_client_ids:
        client_id += 1

    print(f"Your client ID is {client_id}")

    username = input("Please insert username")
    while username in username_check():
        username = input("Username already exists. Please insert different username")

    password = input("Please insert password")

    client = Client(client_id, username, password)
    print(f"Account created with username: {username} and password: {password}")
    client.represent(client_id, username)
    add_account_query = "INSERT INTO Clients (ClientID, Username, Password) VALUES (%s, %s, %s)"
    account_data = (client_id, username, password)

    db_query(connection, add_account_query, account_data)
    connection.commit()


def make_deposit():
    print("In order to make a deposit, please log into your account")
    username = input("Please insert username")
    while username not in username_check():
        username = input("Invalid username. Please insert correct username")
    print("Username correct")

    password = input("Please insert password")

    while password != password_check(username):
        password = input("Invalid Password. Please insert password once again:")

    for i in range(20):

        try:
            deposit = int(input("Please enter amount you would like to deposit:"))
            if deposit == 0:
                print("0 value is not available")
                continue
        except:
            ValueError()
            continue
        break

    transaction_type = "Deposit"
    add_transaction_query = "INSERT INTO Transactions (Username, DepositDate, DepositAmount, TransactionType) VALUES (%s, %s, %s, %s)"
    transaction_data = (username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), deposit, transaction_type)
    db_query(connection, add_transaction_query, transaction_data)
    connection.commit()


def withdraw_funds():
    print("In order to make a withdrawal, please log into your account")
    username = input("Please insert username")
    while username not in username_check():
        username = input("Invalid username. Please insert correct username")
    print("Username correct")

    password = input("Please insert password")

    while password != password_check(username):
        password = input("Invalid Password. Please insert password once again:")

    all_transactions = f"SELECT * FROM Transactions WHERE Username = '{username}'"
    total_balance = 0
    for i in db_query(connection, all_transactions):
        total_balance += i[2]

    print(total_balance)

    for i in range(20):

        try:
            withdrawal = int(input("Please enter amount you would like to withdraw:"))
            if withdrawal == 0:
                print("0 value is not available")
                continue
            elif withdrawal > total_balance:
                print("Not enough funds in balance for withdrawal")
                continue
        except:
            ValueError()
            continue
        break

    withdrawal = -withdrawal
    transaction_type = "Withdrawal"
    add_transaction_query = "INSERT INTO Transactions (Username, DepositDate, DepositAmount, TransactionType) VALUES (%s, %s, %s, %s)"
    transaction_data = (username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), withdrawal, transaction_type)

    db_query(connection, add_transaction_query, transaction_data)
    connection.commit()


def list_all_accounts():
    list_accounts = "SELECT * FROM Clients"

    for x in db_query(connection, list_accounts):
        print(x)


def main_menu():
    print("Please select number for following process")
    print("1. Create account")
    print("2. Make Deposit")
    print("3. Withdraw funds")
    print("4. List all accounts")
    print("5. Calculate balances of all users")
    print("6. Exit the program")


def handle_choice(choice):
    if choice == "1":
        print("Creating account...")
        create_account()
    elif choice == "2":
        print("Making Deposit...")
        make_deposit()
    elif choice == "3":
        print("Withdraw funds...")
        withdraw_funds()
    elif choice == "4":
        print("Listing data...")
        list_all_accounts()
    elif choice == "5":
        print("Exiting the program.")
    elif choice == "6":
        print("Exiting the program.")
        quit()

    else:
        print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    while True:
        main_menu()
        while True:
            try:
                user_choice = input("Enter your choice: ")
                handle_choice(user_choice)
            except EOFError:
                print('End of file reached unexpectedly.')
