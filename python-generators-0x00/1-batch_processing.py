#!/usr/bin/python3
"""
Batch processing functions using generators for memory-efficient data processing
"""
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that yields batches of user data
    Each batch contains batch_size number of users
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

        offset = 0

        while True:
            # Fetch batch of users
            cursor.execute("""
                SELECT user_id, name, email, age
                FROM user_data
                LIMIT %s OFFSET %s
            """, (batch_size, offset))

            batch = cursor.fetchall()

            # If no more data, break
            if not batch:
                break

            # Yield the batch
            yield batch

            # Move to next batch
            offset += batch_size

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


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    Uses no more than 3 loops total
    """
    try:
        # First loop: iterate through batches
        for batch in stream_users_in_batches(batch_size):
            # Second loop: iterate through users in batch
            for user in batch:
                # Filter users over age 25
                if user['age'] > 25:
                    yield user

    except Exception as e:
        print(f"Error in batch processing: {e}")
        return
