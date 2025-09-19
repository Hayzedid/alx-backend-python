#!/usr/bin/python3
"""
Generator function to stream users from database one by one
"""
import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that yields user data one by one from the database
    Uses yield to create a generator for memory-efficient streaming
    """
    connection = None
    cursor = None

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Update with your MySQL username
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)

        # Execute query to fetch all users
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # Yield each row one by one (only one loop as required)
        for row in cursor:
            yield row

    except Error as e:
        print(f"Database error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
