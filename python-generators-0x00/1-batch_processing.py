# File: 1-batch_processing.py

import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to yield users from MySQL in batches."""
    conn = mysql.connector.connect(
        host="localhost",
        user="host",
        password="password",
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    offset = 0

    while True:
        cursor.execute("SELECT user_id, name, email, age FROM users LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Process each batch and print users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            user_dict = {
                'user_id': user[0],
                'name': user[1],
                'email': user[2],
                'age': user[3]
            }
            if user_dict['age'] > 25:
                print(user_dict)
