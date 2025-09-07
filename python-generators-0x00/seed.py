#!/usr/bin/python3
"""
Database seeding script for ALX Python Generators project
"""
import mysql.connector
import csv
import uuid
from mysql.connector import Error


def connect_db():
    """
    Connects to the MySQL database server
    Returns a connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Update with your MySQL username
            password='',  # Update with your MySQL password
            autocommit=True
        )
        print("Connected to MySQL server successfully")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    Returns a connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Update with your MySQL username
            password='',  # Update with your MySQL password
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database successfully")
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist
    """
    try:
        cursor = connection.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Data already exists in the database")
            cursor.close()
            return

        # Read CSV and insert data
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID if not present
                user_id = str(uuid.uuid4())

                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    user_id,
                    row['name'],
                    row['email'],
                    float(row['age'])
                ))

        connection.commit()
        print("Data inserted successfully")
        cursor.close()

    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    except Exception as e:
        print(f"Unexpected error: {e}")
