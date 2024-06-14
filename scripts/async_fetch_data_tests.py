import aiohttp
import asyncio
import logging
import time
import csv
import os

from requests.exceptions import JSONDecodeError
import pandas as pd

# Read data to dataframe
df = pd.read_csv('raw_data.csv', sep=',', decimal='.')

# Bounding box of India coordinates
india_bbox = (68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078)
india_high_lat, india_low_lat = 35.4940095078, 7.96553477623
india_high_long, india_low_long = 97.4025614766, 68.1766451354

# Dropping rows with NaN (although there are no NaNs)
df.dropna(inplace=True)

# Dropping locations outside of bbox
outside_locations_df = df.loc[(df['Restaurant_latitude'] < india_low_lat) |
                              (df['Restaurant_latitude'] > india_high_lat) |
                              (df['Restaurant_longitude'] < india_low_long) |
                              (df['Restaurant_longitude'] > india_high_long) |
                              (df['Delivery_location_latitude'] < india_low_lat) |
                              (df['Delivery_location_latitude'] > india_high_lat) |
                              (df['Delivery_location_longitude'] < india_low_long) |
                              (df['Delivery_location_longitude'] > india_high_long)]

df.drop(outside_locations_df.index, inplace=True)



def setup_logging():
    logger = logging.getLogger(__name__)  # Get a logger for your module
    logger.setLevel(logging.DEBUG)  # Set the logging level

    log_file_path = 'logs/route_problems.log'

    # Check if the directory exists, if not create it
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Create a file handler for writing logs to a file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.ERROR)  # Set the logging level for the file

    # Create a console handler for printing logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the logging level for the console

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if not logging.getLogger().hasHandlers():
    logger = setup_logging()

class OSMR_Client:
    def __init__(self) -> None:
        self.base_url = f'http://router.project-osrm.org/route/v1/driving/'
        self.suffix = '?overview=false&geometries=geojson&steps=true'
        self.route_coordinates = dict()

    async def _fetch_data(self, session, record_idx, start_point, end_point):
        osrm_url = self.base_url + f'{start_point[1]},{start_point[0]};{end_point[1]},{end_point[0]}' + self.suffix
        try:
            async with session.get(osrm_url) as response:
                response.raise_for_status()
                data = await response.json()
                route_coordinates = [[(point[1], point[0]) for point in data['routes'][0]['legs'][0]['steps'][i]['geometry']['coordinates']] for i in range(len(data['routes'][0]['legs'][0]['steps']))]
                distance = round(data['routes'][0]['distance']/1000, ndigits=4)
                self.route_coordinates[record_idx] = (route_coordinates, distance)
        except (aiohttp.ClientError, JSONDecodeError) as error:
            logger.exception(f"Index: {record_idx}. Error: {error}. Route for points: start {start_point}, end {end_point}")

    async def get_routes(self, record_idxs, start_points, end_points, ):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for start_point, end_point, record_idx in zip(start_points, end_points, record_idxs):
                await asyncio.sleep(0.30)
                task = asyncio.create_task(self._fetch_data(session, record_idx, start_point, end_point))
                tasks.append(task)
            return await asyncio.gather(*tasks, return_exceptions=True)

client = OSMR_Client()
# messed indices from last run
indices = [29661, 29681, 29656, 29651, 29639, 29682, 29662, 29687,
           29690, 29653, 29691, 29670, 29669, 29674, 29672, 29676,
           29671, 29678, 29675, 29673, 29680, 29677, 29679, 29692]
df = df.loc[indices]

async def main():
    start_points = [(y1, x1) for x1, y1 in zip(df['Restaurant_longitude'], df['Restaurant_latitude'])]
    end_points = [(y2, x2) for x2, y2 in zip(df['Delivery_location_longitude'], df['Delivery_location_latitude'])]
    record_idxs = df.index
    await client.get_routes(record_idxs, start_points, end_points)
    result_path = "routes/routes3.csv"
    result_dir = os.path.dirname(result_path)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    with open(result_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=("Og-data-row-number", "Route-coordinates", "Distance [km]"))
        writer.writeheader()
        for key, val in client.route_coordinates.items():
            writer.writerow({"Og-data-row-number": key, "Route-coordinates": val[0], "Distance [km]":val[1]})


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    stop = time.time()
    print("TIME: ", stop-start)
