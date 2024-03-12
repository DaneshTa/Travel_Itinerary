import sqlite3

try:
    # Connect to your SQLite database
    conn = sqlite3.connect('my_database.db')
    print("Connected to SQLite")

    # Execute a query to fetch the names of all tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    # Print the list of table names
    print("List of tables:")
    for table in table_names:
        print(table[0])

    # Define the table names
    table_names = ['places', 'tours', 'products','cities']

    # Print the list of table names
    print("List of tables:")
    for table_name in table_names:
        print(table_name)
        # Execute a query to fetch the column names of the table
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        # Execute a query to fetch the first 10 rows of the table
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
        rows = cursor.fetchall()

        # Print the fetched rows with headers
        print(column_names)  # Print column headers
        for row in rows:
            print(row)

except sqlite3.Error as error:
    print("Failed to execute the query:", error)

finally:
    if conn:
        conn.close()
        print("SQLite connection closed")
