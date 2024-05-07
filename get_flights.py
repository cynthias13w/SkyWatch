import configparser
import pandas as pd
import operations
from datetime import datetime, timedelta
import pymongo

config = configparser.ConfigParser()
config.read('config.ini')
mongo_client = pymongo.MongoClient(config['MONGO_DB']['MONGO_CLIENT'])
db = mongo_client['SkyWatch']
collection = db['flights']

iata_codes = pd.read_csv('iata_codes.csv')

france = iata_codes.loc[iata_codes['Country'] == 'France']
spain = iata_codes.loc[iata_codes['Country'] == 'Spain']
germany = iata_codes.loc[iata_codes['Country'] == 'Germany']
italy = iata_codes.loc[iata_codes['Country'] == 'Italy']
uk = iata_codes.loc[iata_codes['Country'] == 'United Kingdom']

def fetch_and_save(origin_code, destiny_code, date):
    print('trying to get flights: ' + origin_code + ' - ' + destiny_code + ' at ' + date.strftime('%Y-%m-%d'))
    data = operations.get_flight_schedules(origin_code, destiny_code, date.strftime('%Y-%m-%d'))
    if data != 'invalid request':
        collection.insert_one(data)
        print('Data saved: ' + origin_code + ' - ' + destiny_code)

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




