import pandas as pd
import ast
from scripts.clusters import cluster_city

'''
Inputs: routes2.csv (data from OSM API), clusters.csv (mapping of each route to a city)
Make routes unique and flattened (list of points), obtain their count.
'''

df_routes = pd.read_csv('routes2.csv', delimiter=',')
df_clusters = pd.read_csv('clusters.csv', delimiter=',')

df_routes = df_routes.merge(df_clusters, on="Og-data-row-number", how='inner')

unique_routes = df_routes.drop_duplicates(subset='Route-coordinates')
route_counts = df_routes['Route-coordinates'].value_counts().reset_index()
route_counts.columns = ['Route-coordinates', 'count']
unique_routes = unique_routes.merge(route_counts, on='Route-coordinates', how='left')


df_routes = unique_routes['Route-coordinates'].apply(lambda x: ast.literal_eval(x)).to_list()
flat_list_of_routes = [[point for route_fragment in route for point in route_fragment] for route in df_routes]

flat_routes = pd.Series(flat_list_of_routes, name="Route-coordinates")
unique_routes["Route-coordinates"] = flat_routes
unique_routes.to_csv('unique_flat_routes.csv', index=False)