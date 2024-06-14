'''
Idea was to inject some javascript code, so that Folium would lazyload only in certain range. Didn't work. Ultimately we managed to reduce number of routes, so script became obsolete.
'''

# import folium
# from folium.plugins import MarkerCluster
# center_eendia_point = (21.9149, 78.0281)
# # Create a map

# # Define a JavaScript function for lazy loading data
# js_code = """
# // Function to load additional data when the map is moved or zoomed
# function loadData() {
#     // Check if the map view has changed significantly
#     // You can adjust the threshold values based on your requirements
#     if (map.getBounds().getNorthEast().distanceTo(map.getBounds().getSouthWest()) > 10000) {
#         // Load additional data via AJAX or other methods
#         // For demonstration purposes, we'll just add a marker
#         var marker = L.marker([51.5, -0.1]).addTo(map);
#     }
# }

# // Add event listeners to trigger the loadData function
# map.on('moveend', loadData);
# map.on('zoomend', loadData);
# """

# def make_map_lazy_load():
#     import folium
#     import json

#     # Read GeoJSON data
#     with open('all_routes.geojson') as f:
#         geojson_data = json.load(f)

#     # Create a Folium map
#     m = folium.Map(location=center_eendia_point, zoom_start=10)

#     # Add GeoJSON layer to the map
#     folium.GeoJson(geojson_data, style_function=lambda feature:{"color":"blue"}).add_to(m)
#     js_obj = folium.JavascriptLink(js_code)
#     m.add_child(js_obj)

#     # Display the map
#     m.save('map_with_geojson_lazy_loading.html')


# if __name__ == "__main__":
#     make_map_lazy_load()


import folium
from folium.plugins import MarkerCluster

# Create a map
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

# Define a JavaScript function for lazy loading data
js_code = """
// Function to load additional data when the map is moved or zoomed
function loadData() {
    // Check if the map view has changed significantly
    // You can adjust the threshold values based on your requirements
    if (this.getBounds().getNorthEast().distanceTo(map.getBounds().getSouthWest()) > 100) {
        // Load additional data via AJAX or other methods
        // For demonstration purposes, we'll just add a marker
        var marker = L.marker([51.5, -0.1]).addTo(map);
    }
}

// Add event listeners to trigger the loadData function
map.on('moveend', loadData);
map.on('zoomend', loadData);

// Initial load of data
loadData();
"""

m.get_root().html.add_child(folium.Element(f"<script>{js_code}</script>"))

# Display the map
# m.save("lazy_loading_map.html")

