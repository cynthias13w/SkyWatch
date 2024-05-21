import configparser
import pandas as pd
import operations
from datetime import datetime, timedelta
import pymongo
import time
from collections import deque

config = configparser.ConfigParser()
config.read('config.ini')
mongo_client = pymongo.MongoClient(config['MONGO_DB']['MONGO_CLIENT'])
db = mongo_client['SkyWatch']
collection = db['flights']

iata_codes = pd.read_csv('iata_codes.csv')

# list of countries to import 
france = iata_codes.loc[iata_codes['Country'] == 'France']
spain = iata_codes.loc[iata_codes['Country'] == 'Spain']
germany = iata_codes.loc[iata_codes['Country'] == 'Germany']
italy = iata_codes.loc[iata_codes['Country'] == 'Italy']
uk = iata_codes.loc[iata_codes['Country'] == 'United Kingdom']

# Define rate limits
MAX_CALLS_PER_SECOND = 6
MAX_CALLS_PER_HOUR = 1000

# Track timestamps of requests
second_timestamps = deque()
hour_timestamps = deque()

def wait_for_rate_limit():
    current_time = time.time()

    # Remove timestamps older than 1 second from the second_timestamps queue
    while second_timestamps and second_timestamps[0] <= current_time - 1:
        second_timestamps.popleft()

    # Remove timestamps older than 1 hour from the hour_timestamps queue
    while hour_timestamps and hour_timestamps[0] <= current_time - 3600:
        hour_timestamps.popleft()

    # Check if adding a new request would exceed the per-second limit
    if len(second_timestamps) >= MAX_CALLS_PER_SECOND:
        sleep_time = 1 - (current_time - second_timestamps[0])
        time.sleep(sleep_time)
        wait_for_rate_limit()  # Recursive call to check again after sleep
        return

    # Check if adding a new request would exceed the per-hour limit
    if len(hour_timestamps) >= MAX_CALLS_PER_HOUR:
        sleep_time = 3600 - (current_time - hour_timestamps[0])
        time.sleep(sleep_time)
        wait_for_rate_limit()  # Recursive call to check again after sleep
        return
    

def fetch_and_save(origin_code, destiny_code, date):
    # check for rate limit 
    wait_for_rate_limit()

    print('trying to get flights: ' + origin_code + ' - ' + destiny_code + ' at ' + date.strftime('%Y-%m-%d'))
    data = operations.get_flight_schedules(origin_code, destiny_code, date.strftime('%Y-%m-%d'))
    if data != 'invalid request':
        collection.insert_one(data)
        print('Data saved: ' + origin_code + ' - ' + destiny_code)

    # Update timestamps
    current_time = time.time()
    second_timestamps.append(current_time)
    hour_timestamps.append(current_time)
    

try:
    start_date = datetime.today()
    # end_date = start_date + timedelta(days = 365) 
    end_date = start_date + timedelta(days = 3) # using a smaller window of time for testing

    current_date = start_date

    while current_date <= end_date:
        for origin_code in germany['IATA']:
            # Flights within Germany 
            for destiny_code in germany['IATA']:
                if origin_code != destiny_code: # Making sure it is not the same airport
                    fetch_and_save(origin_code, destiny_code, current_date)

            # Flights to France
            for destiny_code in france['IATA']:
                fetch_and_save(origin_code, destiny_code, current_date)

            # Flights to spain
            for destiny_code in spain['IATA']:
                fetch_and_save(origin_code, destiny_code, current_date)

            # Flights to italy
            for destiny_code in italy['IATA']:
                fetch_and_save(origin_code, destiny_code, current_date)

        # increases the day
        current_date += timedelta(days = 1)

    
except Exception as e:
    print(f'Error inserting data into MongoDB: {e}')
finally:
    mongo_client.close()