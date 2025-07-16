# BASE_STATION_PLACEMENT
# 📡 Base Station Placement and Coverage Visualizer


This Python project allows you to **strategically place base stations** (e.g., for telecom, Wi-Fi, or communication networks) within any city or geographic area using OpenStreetMap data. It ensures optimal coverage by choosing high-connectivity nodes on the road network and avoiding overlap using a minimum distance constraint.

The project uses libraries like **GeoPandas**, **OSMnx**, and **Folium** to visualize network placements and simulate coverage regions.

---

## 🚀 Features

- 🔍 Automatically finds high-connectivity nodes from OpenStreetMap
- 📍 Places base stations while maintaining a minimum distance between them
- 🗺️ Visualizes stations on an interactive map
- 📌 Calculates and displays the optimal midpoint (e.g., for placing a central server or tower)
- 🌐 Serves the map via a local web server for easy viewing

---

## 🧠 Use Cases

- Telecom tower placement simulation
- Wireless access point planning
- Urban coverage planning
- Research and educational purposes in GIS or network optimization

---

## 🛠️ Technologies Used

- [OSMnx](https://github.com/gboeing/osmnx)
- [GeoPandas](https://geopandas.org/)
- [Folium](https://python-visualization.github.io/folium/)
- Python Standard Libraries (`http.server`, `math`, `threading`, `tempfile`, `webbrowser`)

---

## ⚙️ Installation

Make sure you have Python 3.x installed.

