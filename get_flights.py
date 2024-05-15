import configparser
import pandas as pd
import operations
import pymongo
import json

import time
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')
mongo_client = pymongo.MongoClient(config['MONGO_DB']['MONGO_CLIENT'])
db = mongo_client['SkyWatch']
collection = db['flights']

def get_country_iata_codes(country):
    iata_codes = pd.read_csv('iata_codes.csv')
    return iata_codes.loc[iata_codes['Country'] == country]

country = get_country_iata_codes(input("Enter the country: "))

date=datetime.today()

# Rate limit constants
MAX_CALLS_PER_SECOND = 6
MAX_CALLS_PER_HOUR = 1000

# Track the number of API calls made in the current second and hour
calls_this_second = 0
calls_this_hour = 0
hour_start_time = datetime.now()

def fetch_and_save(origin_code, destiny_code, date):
    print('✈️ Fetching flights: ' + origin_code + ' - ' + destiny_code + ' at ' + date.strftime('%Y-%m-%d'))
    data = operations.get_flight_schedules(origin_code, destiny_code, date.strftime('%Y-%m-%d'))
    if data != 'invalid request':
        collection.insert_one(data)
        with open('output.json', "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f'💾 Data Saved for {origin_code} - {destiny_code}')


try:
    start_date = datetime.today()
    end_date = start_date + timedelta(days=365)

    current_date = start_date

    while current_date <= end_date:
        for origin_code in country['IATA']:
            for destiny_code in country['IATA']:
                if origin_code != destiny_code: # Making sure it is not the same airport
                     # Rate limiting logic
                    current_time = datetime.now()
                    if current_time - hour_start_time >= timedelta(hours=1):
                        calls_this_hour = 0
                        hour_start_time = current_time
                    if calls_this_second >= MAX_CALLS_PER_SECOND:
                        time.sleep(1)  # Wait for a second if the rate limit is reached
                        calls_this_second = 0
                    if calls_this_hour >= MAX_CALLS_PER_HOUR:
                        print('1000 calls per hour limit reached')
                        break

                    # Call the API
                    fetch_and_save(origin_code, destiny_code, current_date)

        # Next day
        current_date += timedelta(days=1)


except Exception as e:
    print(f'Error inserting data into MongoDB: {e}')
finally:
    mongo_client.close()
