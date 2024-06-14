'''
Inputs: interpolated_routes.csv
Outputs: <image>.png

Somewhat works, but bad for visualization.
'''

from PIL import Image
import numpy as np
import pandas as pd
import ast
from clusters import cluster_city
import matplotlib.pyplot as plt

def create_heatmap(coordinates, resolution, heatmap):

    # Calculate bin size
    lat_range = max_lat - min_lat
    lon_range = max_lon - min_lon
    lat_step = lat_range / resolution
    lon_step = lon_range / resolution

    # Iterate through coordinates and increment pixel values
    for lat, lon in coordinates:
        x = int((lon - min_lon) / lon_step)
        y = int((lat - min_lat) / lat_step)
        if 0 <= x < resolution and 0 <= y < resolution:
            heatmap[y, x] += 1


# load routes and create
# Og-data-row-number, Route-coordinates, Distance [km], cluster_n, count,
df_routes = pd.read_csv('interpolated_routes.csv', delimiter=',', index_col=False)

# split dataframes to different cities
for cluster in cluster_city.keys(): # Mumbai temporarily
    df_city = df_routes[df_routes['cluster_n'] == cluster].drop(columns=['cluster_n'])
    cities = df_city

    # Image resolution
    resolution = 4000  # Adjust as needed

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

    # Initialize an empty array to accumulate counts
    heatmap = np.zeros((resolution, resolution), dtype=np.uint32)
    for i, str_route_coords in enumerate(cities["Route-coordinates"]):
        route_coords = ast.literal_eval(str_route_coords)
        
        # Create heatmap for all sets
        create_heatmap(route_coords, resolution, heatmap)

    # normalize pixel values
    min_value = np.min(heatmap)
    max_value = np.max(heatmap)
    heatmap_normalized = (255 * ((heatmap - min_value) / (max_value - min_value))).astype(np.uint8)

    zero_mask = np.flipud((heatmap == 0))
    expanded_zero_mask = np.expand_dims(zero_mask, axis=-1)
    heatmap_normalized = np.flipud(heatmap_normalized.astype(np.uint8))


    cm = plt.get_cmap('cool')
    inferno_heatmap = cm(heatmap_normalized)
    inferno_image_rgba = (inferno_heatmap[:, :, :3] * 255).astype(np.uint8)
    inferno_image_rgba = np.where(expanded_zero_mask, 255, inferno_image_rgba)
    inferno_image = Image.fromarray(inferno_image_rgba)


    # Save the image
    inferno_image.save(f'images/{cluster_city[cluster]}_food_deliveries_heatmap.png')
