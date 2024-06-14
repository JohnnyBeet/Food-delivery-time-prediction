'''
Makes folium map but with geojson instead of dataframe. Only for reference.
'''

center_eendia_point = (21.9149, 78.0281)

def make_json():
    # saving data to geojson
    import geojson
    import ast
    import pandas as pd

    def single_route_to_geojson(coordinates: list[list[tuple]]):
        route = []
        for sublist in coordinates[:-1]:    #API returned double endpoint at the end. Messes geojson
            inverted_coords = [(lon, lat) for lat, lon in sublist]
            route.extend(inverted_coords)
        polygon = geojson.LineString(route)
        feature = geojson.Feature(geometry=polygon)
        return feature

    df_routes = pd.read_csv('routes2.csv', delimiter=',')
    routes = df_routes['Route-coordinates']

    all_features = []
    for str_route in routes:
        route = ast.literal_eval(str_route)
        all_features.append(single_route_to_geojson(route))

    geojson_data = geojson.FeatureCollection(all_features)

    # Save all routes as one GeoJSON file
    with open("all_routes.geojson", "w") as f:
        geojson.dump(geojson_data, f, sort_keys=True)


def make_map_from_json():
    import folium
    import json

    # Read GeoJSON data
    with open('all_routes.geojson') as f:
        geojson_data = json.load(f)

    # Create a Folium map
    m = folium.Map(location=center_eendia_point, zoom_start=10)

    # Add GeoJSON layer to the map
    folium.GeoJson(geojson_data, style_function=lambda feature:{"color":"blue"}).add_to(m)

    # Display the map
    m.save('webpages/map_with_geojson.html')


if __name__=="__main__":
    # make_json()
    make_map_from_json()
