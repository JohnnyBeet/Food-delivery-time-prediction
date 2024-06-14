'''
Inputs: unique_flat_routes.csv (this is csv that contains only unique routes as list of tuples (hence flat) with their counts (how many times they occur)).
Outputs: interpolated_routes.csv

What does it do: for every route it does linear interpolation, so that between two points there is 5m or less. Format the same as input, only routes lists changes.
'''

from geopy.distance import geodesic
import pandas as pd
import ast

#https://stackoverflow.com/questions/65706264/pandas-dataframe-interpolate-gps-coordintes-in-order-to-have-data-every-1-second

from geopy.distance import geodesic

def calculate_distance(coord1, coord2):
    """Calculate distance between two geographic coordinates."""
    return geodesic(coord1, coord2).meters

def interpolate_points(coord1, coord2, threshold):
    """Interpolate between two points if the distance between them exceeds the threshold."""
    distance = calculate_distance(coord1, coord2)
    if distance > threshold:
        # Interpolate
        num_points = int(distance // threshold)
        lats = [coord1[0] + (coord2[0] - coord1[0]) * i / num_points for i in range(1, num_points)]
        lons = [coord1[1] + (coord2[1] - coord1[1]) * i / num_points for i in range(1, num_points)]
        interpolated_points = [(lat, lon) for lat, lon in zip(lats, lons)]
        return interpolated_points
    else:
        return []


def process_points(points, threshold):
    """Process list of points and interpolate if needed."""
    interpolated_points = []
    
    for i in range(len(points) - 1):
        coord1 = points[i]
        coord2 = points[i + 1]
        distance = calculate_distance(coord1, coord2)
        interpolated_points.append(coord1)
        if distance > threshold:
            interpolated_points.extend(interpolate_points(coord1, coord2, threshold))
    
    # Add the last point
    interpolated_points.append(points[-1])
    
    return interpolated_points


threshold = 5  # Threshold in meters
unique_routes = pd.read_csv('unique_flat_routes.csv', converters={"Route-coordinates": ast.literal_eval}, index_col=False)
routes = unique_routes["Route-coordinates"]
for idx, route in enumerate(routes):
    interpolated_points = process_points(route, threshold)
    unique_routes.at[idx, 'Route-coordinates'] = interpolated_points

unique_routes.to_csv('interpolated_routes.csv', index=False)
