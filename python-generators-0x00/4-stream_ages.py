# File: 4-stream_ages.py

import seed  # Assumes this provides connect_to_prodev()

def stream_user_ages():
    """Generator that yields one age at a time from the user_data table."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row['age']
    
    connection.close()


def calculate_average_age():
    """Computes the average age of users using a generator without loading all data."""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")
