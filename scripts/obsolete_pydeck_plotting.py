'''
Drawing map using pydeck, wrapper for deck.gl. Had some trobules with it, as it produces around 1.5GB of data...

Was supposed to help with processing large data. Didn't help. No special visualization assets for routes. Obsolete.
'''

import pydeck as pdk
import json

# Example GeoJSON route data
with open('all_routes.geojson') as f:
    geojson_data = json.load(f)

# Define a GeoJSONLayer for rendering routes
layer = pdk.Layer(
    'GeoJsonLayer',
    data=geojson_data,
    get_line_color=[255, 0, 0],  # Red color for routes
    get_line_width=5,
    line_join_round=True
)

# Create a map visualization
view_state = pdk.ViewState(
    longitude=-122.4194,
    latitude=37.7749,
    zoom=12
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state
)

# Render the map
deck.to_html('webpages/deck.html')
