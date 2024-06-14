'''
Inputs: interpolated_routes.csv
Outputs: map_with_point.html

What does it do: creates html map with points for every route. Unused really, but needed for reference.
'''

import folium
import pandas as pd
import ast

df_routes = pd.read_csv('..\interpolated_routes.csv', delimiter=',', converters={"Route-coordinates": ast.literal_eval}, index_col=False)

routes = df_routes['Route-coordinates']
center_eendia_point = (21.9149, 78.0281)

# Create a map centered around the start point
mymap = folium.Map(location=center_eendia_point, zoom_start=6, prefer_canvas=True)
marker_group = folium.FeatureGroup(name='Routes')  # Create a FeatureGroup for markers

for route in routes:
    [folium.CircleMarker(location=point, radius=2, color='rgba(0, 0, 255)', fill=True, weight=0.5).add_to(marker_group) for point in route]

# Add the marker group to the map
marker_group.add_to(mymap)

# Add layer control to the map
folium.LayerControl().add_to(mymap)

# Save the map to an HTML file
mymap.save("webpages/map_with_points.html")
