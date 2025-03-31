import mysql.connector
from mysql.connector import Error


def db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Fixed capitalization of "Localhost" to "localhost"
            user="root",
            password="root5",
            database="igamingapp"
        )
        print("Connection Successful to DB")
    except Error as e:
        print(f"The error {e} occurred")
    return connection


def db_query(connection, query, data=None):
    my_cursor = connection.cursor()
    try:
        my_cursor.execute(query, data)
        connection.commit()  # Ensure changes are committed
        print("Operation executed")
    except Error as e:
        print(f"The error {e} occurred")
    return my_cursor


# Queries to create tables
create_table_query = """
CREATE TABLE IF NOT EXISTS Clients (
    ClientID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(50)
)
"""

create_table2_query = """
CREATE TABLE IF NOT EXISTS Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255),
    DepositAmount INT,
    DepositDate DATETIME,
    TransactionType VARCHAR(50),
    FOREIGN KEY (Username) REFERENCES Clients(Username)
)
"""

# Establishing the connection
connection = db_connection()

# Execute the queries
if connection:
    db_query(connection, create_table_query)
    db_query(connection, create_table2_query)