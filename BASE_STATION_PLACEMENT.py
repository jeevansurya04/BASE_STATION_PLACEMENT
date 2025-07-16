import geopandas as gpd
import osmnx as ox
import folium
import webbrowser
import threading
import http.server
import socketserver
import tempfile
import shutil
import os
import time
import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the great-circle distance between two points
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Step 1: Load map data and base stations
def get_base_stations(place_name, num_stations=10, min_dist_km=0.5):
    area = ox.geocode_to_gdf(place_name)
    area = area.to_crs(epsg=3857)
    G = ox.graph_from_place(place_name, network_type='drive')
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

    area = area.to_crs(epsg=4326)
    center_latlon = [area.geometry.centroid.y.values[0], area.geometry.centroid.x.values[0]]
    mymap = folium.Map(location=center_latlon, zoom_start=13)

    node_degree = dict(G.degree)
    sorted_nodes = sorted(node_degree, key=node_degree.get, reverse=True)
    base_stations = []

    for node_id in sorted_nodes:
        node = nodes.loc[node_id]
        lat, lon = node['y'], node['x']
        # Check if this node is far enough from all selected stations
        if all(haversine(lat, lon, s[0], s[1]) >= min_dist_km for s in base_stations):
            base_stations.append((lat, lon))
            folium.Marker(location=[lat, lon], popup="Base Station").add_to(mymap)
        if len(base_stations) >= num_stations:
            break

    return mymap, base_stations

# Step 2: Find midpoint
def find_midpoint(base_stations):
    avg_lat = sum(station[0] for station in base_stations) / len(base_stations)
    avg_lon = sum(station[1] for station in base_stations) / len(base_stations)
    return avg_lat, avg_lon

# Step 3: Draw lines and midpoint
def visualize_network(mymap, base_stations, midpoint):
    folium.Marker(location=midpoint, popup="Optimal Midpoint", icon=folium.Icon(color="red")).add_to(mymap)
    for station in base_stations:
        folium.PolyLine([station, midpoint], color="green").add_to(mymap)
    return mymap

# Step 4: Serve temp file
def start_server(directory, port=8000):
    os.chdir(directory)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving map at http://localhost:{port}/temp_map.html")
        httpd.serve_forever()

# === Main Execution ===
if __name__ == "__main__":
    place_name = input("Enter the city or place name: ")
    mymap, base_stations = get_base_stations(place_name)
    midpoint = find_midpoint(base_stations)
    mymap = visualize_network(mymap, base_stations, midpoint)

    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_map_path = os.path.join(temp_dir, "temp_map.html")
    mymap.save(temp_map_path)

    # Start local server in background
    threading.Thread(target=start_server, args=(temp_dir,), daemon=True).start()
    time.sleep(1)  # Wait a moment for server to spin up

    webbrowser.open("http://localhost:8000/temp_map.html")

    print(f"✅ Map is being served at http://localhost:8000/temp_map.html")
