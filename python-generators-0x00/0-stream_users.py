#!/usr/bin/env python3
import mysql.connector

def stream_users():
    """Generator that yields one row at a time from the user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="YourStrongPassword",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()