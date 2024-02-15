import sqlite3
import csv

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create a table for Points of Interest (POI)
interest = '''PointOfInterest'''
cursor.execute('''
    CREATE TABLE %s (
        POIID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_du_POI VARCHAR(100),
        Categories_de_POI VARCHAR(50),
        
        Latitude REAL,
        Longitude REAL
    )
''' % interest)

# Read data from CSV file and insert into the database
csv_file_path = '/Users/macdanesh/PycharmProjects/HolidayIterny/venv/DataCollection/datatourisme-tour-20240109.csv'
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')  # Adjust delimiter if needed
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO %s (Nom_du_POI, Categories_de_POI, Latitude, Longitude)
            VALUES (?, ?, ?, ?)
        ''' % interest, (row['Nom_du_POI'], row['Categories_de_POI'], row['Latitude'], row['Longitude']))




# Commit changes
conn.commit()

# Query and print the first 20 rows
cursor.execute('SELECT * FROM %s LIMIT 50' % interest)
rows = cursor.fetchall()
for row in rows:
    print(row)


# Close the connection
conn.close()
