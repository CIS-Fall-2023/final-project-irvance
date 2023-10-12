import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None #puts connection on stack, None = no value, means connection on the stack points to nowhere 
    #try = error handling statement to help prevent crashes, takes more processing power, runs twice as slow, try and except any code that could blow up
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )

        print("Connection to MYSQL DB successful.")
    except Error as e:
        print(f"The error '{e} has occured.")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor() #cursor is a vehicle, give it a query to deliver to database
    try:
        cursor.execute(query)
        connection.commit()
        print("Connection to MySQL DB successfuly.")
    except Error as e:
        print(f"The error '{e} has occured.")

def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary = True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    except Error as e:
        print(f"The error '{e} has occured.")