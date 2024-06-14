import osmnx as ox
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import ast
from clusters import cluster_city

'''
Inputs: interpolated_routes.csv
Outputs: <city_name>_routes.png

What does it do:
    For every city in clusters:
        1. create route graph with osmnx and convert it to geopandas dataframe.
        2. create list of gdfs for every route in given city
        3. plot graph-gdf and it routes in gray color
        4. plot every route on the same scales in blue color (density is defined as normalized route count plotted to the power of two (keeps it in [0;1] but pales lower counts))

Title and legend looks really bad, so i skip it.
'''


# load routes and create
# Og-data-row-number, Route-coordinates, Distance [km], cluster_n, count,
df_routes = pd.read_csv('interpolated_routes.csv', delimiter=',', index_col=False)

# split dataframes to different cities
# cities = {}
for cluster in cluster_city.keys(): # Mumbai temporarily
    df_city = df_routes[df_routes['cluster_n'] == cluster].drop(columns=['cluster_n'])
    cities = df_city


    # Initialize min and max values
    min_lat = float('inf')
    max_lat = float('-inf')
    min_lon = float('inf')
    max_lon = float('-inf')

    # Iterate over all routes
    for i, str_route_coords in enumerate(cities["Route-coordinates"]):
        route = ast.literal_eval(str_route_coords)
        for point in route:
            lat, lon = point
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)

    bbox = (max_lat, min_lat, max_lon, min_lon)

    graph = ox.graph_from_bbox(bbox=bbox, network_type='all')


    # Convert the road network to a GeoDataFrame
    gdf = ox.graph_to_gdfs(graph, nodes=False)

    # list of route duplicates for color intensity
    counts = []

    # Create GeoDataFrame for each route
    routes_gdfs = []
    for i, (str_route_coords, count) in enumerate(zip(cities["Route-coordinates"], cities["count"])):
        route_coords = ast.literal_eval(str_route_coords)
        swapped_coords = [(y, x) for x, y in route_coords] # invert to align with city
        route_geom = LineString(swapped_coords)
        route_gdf = gpd.GeoDataFrame(geometry=[route_geom], crs=gdf.crs)
        routes_gdfs.append(route_gdf)
        counts.append(count)

    # get max from count to specify divisor for alpha parameter
    max_count = max(counts)

    # Plot the road network without routes
    ax = gdf.plot(color='#cecece', linewidth=0.1)

    # Plot each route with blue color
    for route_gdf, count in zip(routes_gdfs, counts):
        route_gdf.plot(ax=ax, color=('#002dff', (count/max_count)**2), linewidth=0.1)

    # Show the plot
    # plt.show()
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'images/{cluster_city[cluster]}_food_delivery_graph_map.png', format='png', bbox_inches='tight', pad_inches=0, dpi=1000)
    plt.close()