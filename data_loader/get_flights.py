import pandas as pd
from datetime import datetime, timedelta
from collections import deque
from data_management import *

iata_codes = pd.read_csv('iata_codes.csv')

try:
    # time window
    start_date = datetime.today()
    end_date = start_date + timedelta(days = 20) # using a smaller window of time for testing
    # list of countries to import
    countries_list = ['France', 'Germany', 'Spain', 'Italy', 'Denmark', 'USA', 'United Kingdom', 'Turkey']
    countries_df = iata_codes.loc[iata_codes['Country'].isin(countries_list)]
    countries_df = countries_df.sort_values(by=['Country', 'IATA'])
    iata_codes = countries_df['IATA'].tolist()
    # Load state if it exists - it means that the script is resuming from a previous run
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
                while current_date <= end_date:
                    if fetch_and_save(origin_code, destiny_code, current_date):
                        current_date += timedelta(days=1)
                    else:
                        current_date = end_date + timedelta(days=1) # finishing the loop to not waste calls

                # Reset current_date after the loop
                current_date = start_date

except Exception as e:
    print(f'Error inserting data into MongoDB: {e}')
finally:
    mongo_client.close()
