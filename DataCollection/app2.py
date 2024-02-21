import sqlite3
import math
import random

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371
    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    # Calculate differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_closest_place(city_latitude, city_longitude):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    # Retrieve all places
    cursor.execute('SELECT POIID, Nom_du_POI, Latitude, Longitude FROM places')
    places = cursor.fetchall()
    closest_place = None
    min_distance = float('inf')

    for place_id, place_name, place_latitude, place_longitude in places:
        distance = haversine(city_latitude, city_longitude, place_latitude, place_longitude)
        if distance < min_distance:
            min_distance = distance
            closest_place = (place_id, place_name)

    return closest_place

# Generate a random city ID (you can replace this with your own method)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM cities')
total_cities = cursor.fetchone()[0]
random_city_id = random.randint(1, total_cities)

# Retrieve the random city details
cursor.execute('SELECT * FROM cities WHERE id = ?', (random_city_id,))
random_city, random_city_latitude, random_city_longitude = cursor.fetchone()

# Retrieve the random city details
print(f"Randomly selected city: {random_city[1]}")


# Find the closest place
closest_place_id, closest_place_name = find_closest_place(random_city_latitude, random_city_longitude)
print(f"Randomly selected city coordinates: Latitude {random_city_latitude}, Longitude {random_city_longitude}")
print(f"Closest place: {closest_place_name}")
