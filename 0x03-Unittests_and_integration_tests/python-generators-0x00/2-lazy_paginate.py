#!/usr/bin/python3
"""
Lazy pagination implementation using generators
"""
import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Helper function to fetch a page of users from the database
    """
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Update with your MySQL username
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows

    except Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    """
    Generator function that implements lazy pagination
    Only fetches the next page when needed, starting from offset 0
    Uses only one loop as required
    """
    offset = 0

    while True:
        # Fetch current page
        page = paginate_users(page_size, offset)

        # If no more data, stop
        if not page:
            break

        # Yield the current page
        yield page

        # Move to next page
        offset += page_size
