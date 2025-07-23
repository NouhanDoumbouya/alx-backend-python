import sqlite3

class DatabaseConnection:
    """Context manager for handling database connections."""

    def __init__(self, db_name=db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, trackback):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False
    
# Usage of the context manager
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)