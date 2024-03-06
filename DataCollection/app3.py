import folium
import osmnx as ox
from osmnx import distance
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import math

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

# Define a function to move a point north by a certain distance
def move_north(latitude, distance_in_km):
    # Convert distance to degrees
    distance_in_degrees = (distance_in_km / 111)
    return latitude + distance_in_degrees

# Define a function to move a point west by a certain distance
def move_west(longitude, distance_in_km):
    # Convert distance to degrees
    distance_in_degrees = (distance_in_km / 111 )
    return longitude - distance_in_degrees

# Define a function to get a walking path
def get_walking_path(start_latitude, start_longitude, end_latitude, end_longitude):
    # Get the nearest nodes to the start and end points
    G = ox.graph_from_point((start_latitude, start_longitude), network_type='walk')
    start_node = distance.nearest_nodes(G, start_longitude, start_latitude)
    end_node = distance.nearest_nodes(G, end_longitude, end_latitude)

    # Get the shortest path
    path = ox.shortest_path(G, start_node, end_node)

    # Convert the path to a list of coordinates
    path_coords = [(data['y'], data['x']) for node, data in G.nodes(data=True) if node in path]
    return path_coords

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

    # Move the city's coordinates 1km north and 1km west
    start_latitude = move_north(city_latitude, 1)
    start_longitude = move_west(city_longitude, 1)

    # Find the closest place from the new start point
    closest_place, closest_place_latitude, closest_place_longitude = find_closest_place(start_latitude, start_longitude)

    # Create a map centered at the start point's coordinates
    m = folium.Map(location=[start_latitude, start_longitude], zoom_start=13)

    # Add a marker for the start point
    folium.Marker(
        location=[start_latitude, start_longitude],
        popup="<i>Start Point</i>",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    # Add a marker for the closest place
    folium.Marker(
        location=[closest_place_latitude, closest_place_longitude],
        popup=f"<i>{closest_place[1]}</i>",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    ''' ########################### USE This 1 for walking path
    # Get the walking path
    path_coords = get_walking_path(start_latitude, start_longitude, closest_place_latitude, closest_place_longitude)

    # Draw the path on the map
    folium.PolyLine(path_coords, color="blue").add_to(m)'''

    ########################### OR USE This 2 - Direct line From City to Place
    # Draw a line between the city and the closest place
    folium.PolyLine(locations=[[start_latitude, start_longitude], [closest_place_latitude, closest_place_longitude]], color="blue").add_to(m)

    # Save the map to an HTML file
    m.save("map.html")

    return {
        "random_city_id": city_id,
        "city_name": city.name,
        "city_coordinates": {"latitude": city_latitude, "longitude": city_longitude},
        "closest_place": {"id": closest_place[0], "name": closest_place[1], "coordinates": {"latitude": closest_place_latitude, "longitude": closest_place_longitude}},
        "map": "map.html",
    }
