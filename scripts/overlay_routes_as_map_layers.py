import folium
import pandas as pd
import ast
from clusters import cluster_city

df_routes = pd.read_csv('routes2.csv', delimiter=',')
df_clusters = pd.read_csv('clusters.csv', delimiter=',')

df_routes = df_routes.merge(df_clusters, on="Og-data-row-number", how='inner')

unique_routes = df_routes.drop_duplicates(subset='Route-coordinates')
route_counts = df_routes['Route-coordinates'].value_counts().reset_index()
route_counts.columns = ['Route-coordinates', 'count']
unique_routes = unique_routes.merge(route_counts, on='Route-coordinates', how='left')
clusters = unique_routes['cluster_n']
unique_clusters = clusters.unique()
center_eendia_point = (21.9149, 78.0281)

# Create a map centered around the start point
mymap = folium.Map(location=center_eendia_point, zoom_start=6, prefer_canvas=True)

for cluster in unique_clusters:
    cluster_routes = unique_routes[unique_routes['cluster_n'] == cluster]['Route-coordinates']
    cluster_layer = folium.FeatureGroup(name=f'{cluster_city[cluster]}', show=False)
    for idx, str_route in enumerate(cluster_routes):
        route_coordinates = ast.literal_eval(str_route)
        folium.PolyLine(locations=route_coordinates, color=f"rgba(0, 100, 0, {unique_routes['count'][idx] *0.05})", weight=3).add_to(cluster_layer)
    cluster_layer.add_to(mymap)

# Add layer control to the map
folium.LayerControl().add_to(mymap)

# Save the map to an HTML file
mymap.save("webpages//multilayer_folium_map.html")