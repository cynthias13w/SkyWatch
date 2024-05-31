import os
import json
import pymongo
from collections import deque
from config import settings
import operations

import time
from datetime import datetime


state_file = 'state.json'
mongo_client = pymongo.MongoClient(settings.MONGO_CLIENT)
db = mongo_client[settings.MONGO_DB]
collection = db[settings.MONGO_COLLECTION]

def load_state():
    """
    Load the state from a file.

    :return: The state loaded from the file if the file exists, otherwise None.
    """
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return None

def save_state(state):
    """
    Save the state to a file.

    :param state: The state to be saved.
    """
    with open(state_file, 'w') as f:
        json.dump(state, f)
# Track timestamps of requests
second_timestamps = deque()
hour_timestamps = deque()

def wait_for_rate_limit():
    """
    Waits until it's safe to make a new request based on rate limits.

    This function checks the timestamps of previous requests and sleeps if necessary
    to ensure that the rate limits are not exceeded.
    """
    current_time = time.time()

    # Remove timestamps older than 1 second from the second_timestamps queue
    while second_timestamps and second_timestamps[0] <= current_time - 1:
        second_timestamps.popleft()

    # Remove timestamps older than 1 hour from the hour_timestamps queue
    while hour_timestamps and hour_timestamps[0] <= current_time - 3600:
        hour_timestamps.popleft()

    # Check if adding a new request would exceed the per-second limit
    if len(second_timestamps) >= settings.MAX_CALLS_PER_SECOND:
        sleep_time = 1 - (current_time - second_timestamps[0])
        time.sleep(sleep_time)
        wait_for_rate_limit()  # Recursive call to check again after sleep
        return

    # Check if adding a new request would exceed the per-hour limit
    if len(hour_timestamps) >= settings.MAX_CALLS_PER_HOUR:
        sleep_time = 3600 - (current_time - hour_timestamps[0])
        time.sleep(sleep_time)
        wait_for_rate_limit()  # Recursive call to check again after sleep
        return


def fetch_and_save(origin_code, destiny_code, date):
    """
    Fetches flight schedules for a given origin, destination, and date, and saves the data.

    :param origin_code: The code of the origin airport.
    :param destiny_code: The code of the destination airport.
    :param date: The date for which to fetch flight schedules.
    :return: True if data was fetched and saved successfully, False otherwise.
    """
    # check for rate limit
    wait_for_rate_limit()

    current_time = datetime.now().strftime('%H:%M')
    print(f'Fetching flight: {origin_code} - {destiny_code} on {date.strftime("%Y-%m-%d")} at {current_time}')
    data = operations.get_flight_schedules(origin_code, destiny_code, date.strftime('%Y-%m-%d'))
    if data != 'invalid request':
        collection.insert_one(data)
        print('Data saved: ' + origin_code + ' - ' + destiny_code)
        aux_return = True
    else:
        aux_return = False

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
    return aux_return
