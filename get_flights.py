import configparser
import pandas as pd
import operations
from datetime import datetime, timedelta
import pymongo
import time
from collections import deque
import json
import os

config = configparser.ConfigParser()
config.read('config.ini')
mongo_client = pymongo.MongoClient(config['MONGO_DB']['MONGO_CLIENT'])
db = mongo_client['SkyWatch']
collection = db['flights']

iata_codes = pd.read_csv('iata_codes.csv')

# list of countries to import 
countries_list = ['France', 'Spain', 'Germany', 'Italy']

# Define rate limits
MAX_CALLS_PER_SECOND = 6
MAX_CALLS_PER_HOUR = 1000

# File to save state
state_file = 'state.json'

def load_state():
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return None

def save_state(state):
    with open(state_file, 'w') as f:
        json.dump(state, f)

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

    # Save the state after each fetch and save
    save_state({
        'current_date': date.strftime('%Y-%m-%d'),
        'origin_code': origin_code,
        'destiny_code': destiny_code,
        'second_timestamps': list(second_timestamps),
        'hour_timestamps': list(hour_timestamps)
    })    

try:
    start_date = datetime.today()
    # end_date = start_date + timedelta(days = 365) 
    end_date = start_date + timedelta(days = 3) # using a smaller window of time for testing

    # Load state if it exists
    state = load_state()
    if state:
        current_date = datetime.strptime(state['current_date'], '%Y-%m-%d')
        last_origin_code = state['origin_code']
        last_destiny_code = state['destiny_code']
        second_timestamps = deque(state['second_timestamps'])
        hour_timestamps = deque(state['hour_timestamps'])
    else:
        current_date = start_date
        last_origin_code = None
        last_destiny_code = None

    countries_df = iata_codes.loc[iata_codes['Country'].isin(countries_list)]
    countries_df = countries_df.sort_values(by=['Country', 'IATA'])
    iata_codes = countries_df['IATA'].tolist()

    while current_date <= end_date:

        for origin_code in iata_codes:
            # If resuming, skip to the last saved origin code
            if last_origin_code and origin_code != last_origin_code:
                continue
            last_origin_code = None  # Reset after the first match

            for destiny_code in iata_codes:
                # If resuming, skip to the last saved destiny code
                if last_destiny_code and destiny_code != last_destiny_code:
                    continue
                last_destiny_code = None  # Reset after the first match

                if origin_code != destiny_code:  # Ensure it is not the same airport
                    fetch_and_save(origin_code, destiny_code, current_date)



        # Increase the day
        current_date += timedelta(days=1)



    
except Exception as e:
    print(f'Error inserting data into MongoDB: {e}')
finally:
    mongo_client.close()