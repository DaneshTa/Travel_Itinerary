import folium

# Create a map centered at some coordinates
m = folium.Map(location=[45.5236, -122.6750])

# Save the map to an HTML file
m.save("map.html")
