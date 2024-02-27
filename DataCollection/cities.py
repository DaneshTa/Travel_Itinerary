import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Drop table if it already exists
cursor.execute('''DROP TABLE IF EXISTS cities''')

# Create table
cursor.execute('''CREATE TABLE cities (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    latitude REAL,
                    longitude REAL
                  )''')

# Sample data of 20 cities in France with latitude and longitude
cities_data = [
    ("Paris", 48.8566, 2.3522),
    ("Marseille", 43.2965, 5.3698),
    ("Lyon", 45.7640, 4.8357),
    ("Toulouse", 43.6045, 1.4442),
    ("Nice", 43.7102, 7.2620),
    ("Nantes", 47.2184, -1.5536),
    ("Strasbourg", 48.5734, 7.7521),
    ("Montpellier", 43.6109, 3.8772),
    ("Bordeaux", 44.8378, -0.5792),
    ("Lille", 50.6292, 3.0573),
    ("Rennes", 48.1173, -1.6778),
    ("Reims", 49.2583, 4.0319),
    ("Le Havre", 49.4944, 0.1077),
    ("Saint-Étienne", 45.4397, 4.3872),
    ("Toulon", 43.1242, 5.9280),
    ("Grenoble", 45.1885, 5.7245),
    ("Dijon", 47.3220, 5.0415),
    ("Angers", 47.4784, -0.5632),
    ("Nîmes", 43.8367, 4.3601),
    ("Aix-en-Provence", 43.5297, 5.4474)
]

# Insert data into the table
cursor.executemany("INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)", cities_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created with 20 cities in France.")
