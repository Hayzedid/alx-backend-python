#!/usr/bin/python3
"""
Memory-efficient aggregation using generators to calculate average age
"""
import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator function that yields user ages one by one
    Enables memory-efficient processing of large datasets
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

        cursor = connection.cursor()

        # Execute query to fetch only ages
        cursor.execute("SELECT age FROM user_data")

        # Yield each age one by one
        for row in cursor:
            yield float(row[0])

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


def calculate_average_age():
    """
    Calculate the average age using the generator
    Uses no more than two loops total and doesn't load entire dataset into memory
    """
    total_age = 0
    count = 0

    # First loop: iterate through ages from generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Calculate average
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
        return average_age
    else:
        print("No users found")
        return 0


if __name__ == "__main__":
    # Calculate and display average age when script is run directly
    calculate_average_age()
