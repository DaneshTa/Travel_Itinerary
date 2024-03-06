import sqlite3
import math
import random
import folium
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class City(BaseModel):
    name: str

def get_db_connection():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    return cursor

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
#Not random city instead api call for that

@app.get("/")
async def read_root():
    return {"message": "Welcome to the closest place finder!"}

@app.get("/cities/{city_name}")
def get_city_coordinates(city_name: str):
    cursor = get_db_connection()
    cursor.execute("SELECT latitude, longitude FROM cities WHERE name=?", (city_name,))
    data = cursor.fetchone()
    if data is None:
        return {"error": "City not found"}
    else:
        return {"latitude": data[0], "longitude": data[1]}


@app.post("/closest_place/")
async def get_closest_place(city: City):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Retrieve the city details
    cursor.execute('SELECT id, latitude, longitude FROM cities WHERE name = ?', (city.name,))
    city_id, city_latitude, city_longitude = cursor.fetchone()

    # Find the closest place
    closest_place_id, closest_place_name = find_closest_place(city_latitude, city_longitude)

    return {
        "random_city_id": city_id,
        "city_name": city.name,
        "city_coordinates": {"latitude": city_latitude, "longitude": city_longitude},
        "closest_place": {"id": closest_place_id, "name": closest_place_name}
    }

    # Generate a random city ID
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cities')
    total_cities = cursor.fetchone()[0]
    #random_city_id = random.randint(1, total_cities)

    # Retrieve the random city details
    cursor.execute('SELECT name, latitude, longitude FROM cities WHERE id = ?', (random_city_id,))
    random_city_name, random_city_latitude, random_city_longitude = cursor.fetchone()

    def find_closest_place(city_latitude, city_longitude):
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT POIID, Nom_du_POI, Latitude, Longitude FROM places')
        places = cursor.fetchall()
        closest_place = None
        min_distance = float('inf')
        closest_place_latitude = None
        closest_place_longitude = None

        for place_id, place_name, place_latitude, place_longitude in places:
            distance = haversine(city_latitude, city_longitude, place_latitude, place_longitude)
            if distance < min_distance:
                min_distance = distance
                closest_place = (place_id, place_name)
                closest_place_latitude = place_latitude
                closest_place_longitude = place_longitude

        return closest_place, closest_place_latitude, closest_place_longitude

    # Find the closest place
    (closest_place_id, closest_place_name), closest_place_latitude, closest_place_longitude = find_closest_place(random_city_latitude, random_city_longitude)

    # Find the closest place
    #closest_place_id, closest_place_name = find_closest_place(random_city_latitude, random_city_longitude)
    print(f"Randomly selected city: {random_city_name}")
    print(f"City coordinates: Latitude {random_city_latitude}, Longitude {random_city_longitude}")
    print(f"Closest place: {closest_place_name}")


    # Define a function to move a point north by a certain distance
    def move_north(latitude, distance_in_km):
        # Convert distance to degrees
        distance_in_degrees = (distance_in_km / 111)+5
        return latitude + distance_in_degrees

    # Define a function to move a point west by a certain distance
    def move_west(longitude, distance_in_km):
        # Convert distance to degrees
        distance_in_degrees = (distance_in_km / 111 )+5
        return longitude - distance_in_degrees

    # Move the city's coordinates 1km north and 1km west
    start_latitude = move_north(random_city_latitude, 1)
    start_longitude = move_west(random_city_longitude, 1)

    # Create a map centered at the city's coordinates
    m = folium.Map(location=[random_city_latitude, random_city_longitude], zoom_start=13)

    # Add a marker for the city
    folium.Marker(
        location=[random_city_latitude, random_city_longitude],
        popup=f"<i>{random_city_name}</i>",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    # Add a marker for the closest place
    folium.Marker(
        location=[closest_place_latitude, closest_place_longitude],
        popup=f"<i>{closest_place_name}</i>",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    # Draw a line between the city and the closest place
    folium.PolyLine(locations=[[random_city_latitude, random_city_longitude], [closest_place_latitude, closest_place_longitude]], color="blue").add_to(m)

    # Save the map to an HTML file
    m.save("map.html")