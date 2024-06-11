import certifi
import pymongo
import pandas as pd
from config import settings

client = pymongo.MongoClient(settings.MONGO_URI,tlsCAFile=certifi.where())
total_count = client[settings.DB_NAME][settings.COLLECTION_NAME].count_documents({})

class Schedules:
    def __init__(self):
        self.schedule = []

    def get_data_from_api(self):
        schedulesRes = client[settings.DB_NAME][settings.COLLECTION_NAME].find().limit(25)
        for item in schedulesRes:
            self.schedule.extend(item['ScheduleResource']['Schedule'])
        schedulesdf = pd.DataFrame(self.schedule)
        return schedulesdf

    def transform_df(self):
        schedulesdf = self.get_data_from_api()
        totalJourneydf = pd.json_normalize(schedulesdf['TotalJourney'])
        flightdf = schedulesdf['Flight'].explode()
        durationdf = totalJourneydf['Duration'].repeat(flightdf.groupby(level=0).size())
        schedulesdf = pd.concat([flightdf, durationdf], axis=1).reset_index(drop=True)
        flightdf = pd.json_normalize(schedulesdf['Flight'])
        schedulesdf = pd.concat([flightdf, schedulesdf], axis=1)
        schedulesdf.drop(columns=['Duration', 'MarketingCarrier.AirlineID',
        'MarketingCarrier.FlightNumber', 'Equipment.AircraftCode',
        'Details.Stops.StopQuantity', 'Details.DaysOfOperation',
        'Details.DatePeriod.Effective', 'Details.DatePeriod.Expiration',
        'OperatingCarrier.AirlineID'],inplace=True)
        # schedulesdf.columns = ['Departure', 'Departure Time', 'Departure Terminal', 'Arrival', 'Arrival Time', 'Arrival Terminal', 'Flight']
        schedulesdf.dropna(inplace=True)
        return schedulesdf

    def normalize_df(self):
        schedulesdf = self.transform_df()
        schedulesdf.drop('Flight', inplace=True, axis=1)
        schedules = schedulesdf.to_dict('records')
        return schedules
