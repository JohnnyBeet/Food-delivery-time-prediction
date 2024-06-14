'''
Inputs: routes2.csv (data straight from OSM API)
Outputs: single_layer_map.html

What does it do: creates html map with PolyLines for every route. Unused really, but needed for reference. Limited to 4000 routes, as more cause 
'''

import folium
import pandas as pd
import ast

df_routes = pd.read_csv("routes2.csv", delimiter=',')

routes = df_routes['Route-coordinates'].iloc[:10]
center_eendia_point = (21.9149, 78.0281)

# Create a map centered around the start point
mymap = folium.Map(location=center_eendia_point, zoom_start=6, prefer_canvas=True)
marker_group = folium.FeatureGroup(name='Routes') 
for str_route in routes:
    # Define the OSRM API URL
    route_coordinates = ast.literal_eval(str_route)
    for route_part in route_coordinates:
        [folium.CircleMarker(location=point, radius=2, color='rgba(0, 0, 255)', fill=True, weight=1).add_to(marker_group) for point in route_part]
marker_group.add_to(mymap)
folium.LayerControl().add_to(mymap)

# Save the map to an HTML file
mymap.save("webpages/single_layer_map.html")