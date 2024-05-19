import sqlite3

try:
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('users.db')
    print("Opened database successfully")

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table for users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    print("Table created successfully")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()
        print("Database connection closed")
