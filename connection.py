import mysql.connector
from mysql.connector import Error

# Database connection parameters
db_name = 'ecom'
user = 'root'
password = ''
host = 'localhost'

def connection():
    '''
    Creates and returns a connection to our database.
    '''
    try:
        # Attempt to establish a connection with my DB
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        if conn.is_connected():
            print("Successfully connected to the database!")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None