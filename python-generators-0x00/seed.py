# To create a backend scritp that will seed the database with some initial data

import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    """Connects to the MySQL server (not to a specific database)"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None
    

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev_db():
    """Connects to the ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='norassoba',
            database='ALX_prodev'
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None
    

def create_table(connection):
    """Creates the users table if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        print("Table USER created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Inserts data from a CSV file into the user_data table."""
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully from CSV")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
