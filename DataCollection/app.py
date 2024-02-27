import sqlite3
import math
import random
import folium
import requests

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

    for place_id, place_name, place_latitude, place_longitude in places:
        distance = haversine(city_latitude, city_longitude, place_latitude, place_longitude)
        if distance < min_distance:
            min_distance = distance
            closest_place = (place_id, place_name)

    return closest_place

# Generate a random city ID
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM cities')
total_cities = cursor.fetchone()[0]
random_city_id = random.randint(1, total_cities)

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
'''
####


# Create a map centered at the city's coordinates
m = folium.Map(location=[random_city_latitude, random_city_longitude], zoom_start=13)

# Add a marker for the city
folium.Marker(
    location=[random_city_latitude, random_city_longitude],
    popup=f"{random_city_name}",
    icon=folium.Icon(icon="cloud"),
).add_to(m)



# Assuming you have the coordinates for the closest place
# Add a marker for the closest place
folium.Marker(
    location=[closest_place_latitude, closest_place_longitude],  # replace with actual coordinates
    popup=f"{closest_place_name}",
    icon=folium.Icon(color="red"),
).add_to(m)
'''
##############

# OpenRouteService API url
url = "https://api.openrouteservice.org/v2/directions/foot-walking"

# API parameters
params = {
    'api_key': 'your_api_key',  # replace with your OpenRouteService API key
    'start': f'{random_city_longitude},{random_city_latitude}',
    'end': f'{closest_place_longitude},{closest_place_latitude}'
}

# Send a GET request to the API
response = requests.get(url, params=params)

# Get the route coordinates from the API response
route_coordinates = response.json()['features'][0]['geometry']['coordinates']

# Convert the coordinates to a format that folium can use
route_coordinates = [(lat, lon) for lon, lat in route_coordinates]

# Create a map centered at the city's coordinates
m = folium.Map(location=[random_city_latitude, random_city_longitude], zoom_start=13)

# Add a marker for the city
folium.Marker(
    location=[random_city_latitude, random_city_longitude],
    popup=f"{random_city_name}",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

# Add a marker for the closest place
folium.Marker(
    location=[closest_place_latitude, closest_place_longitude],
    popup=f"{closest_place_name}",
    icon=folium.Icon(color="red"),
).add_to(m)

# Add the route to the map
folium.PolyLine(route_coordinates, color="blue").add_to(m)

# Send a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Try to extract the route coordinates
    try:
        route_coordinates = response.json()['features'][0]['geometry']['coordinates']
    except KeyError:
        print("The response does not contain route coordinates.")
else:
    print(f"API request failed with status code {response.status_code}.")


# Display the map
m.save('map.html')