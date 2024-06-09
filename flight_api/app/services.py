from app.config import settings
from typing import List
import pymongo
from app.models import Flight
from fastapi import Query
from datetime import datetime

client = pymongo.MongoClient(settings.MONGO_URI)

async def get_flight_count():
    total_count = client[settings.DB_NAME][settings.COLLECTION_NAME].count_documents({})
    return {'flight count': f'{total_count}'}


async def get_one_flight():
    cursor = client[settings.DB_NAME][settings.COLLECTION_NAME].find_one()
    return cursor

async def get_flights(
    airport_departure: str = Query(..., description='IATA code of the departure airport'),
    airport_arrival: str = Query(..., description='IATA code of the arrival airport'),
    date_departure: str = Query(..., description='Departure date in YYYY-MM-DD format')
) -> List[Flight]:
    # Ensure the input date is in the correct format
    try:
        datetime.strptime(date_departure, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format. Expected YYYY-MM-DD.')

    query = {
        '$and': [
            {'ScheduleResource.Schedule.Flight.Departure.AirportCode': airport_departure},
            {'ScheduleResource.Schedule.Flight.Arrival.AirportCode': airport_arrival},
            {'ScheduleResource.Schedule.Flight.Departure.ScheduledTimeLocal.DateTime': {'$regex': f'^{date_departure}'}}
        ]
    }
    projection = {
        '_id': 0,  
        'ScheduleResource.Schedule.Flight.Departure.AirportCode': 1,
        'ScheduleResource.Schedule.Flight.Arrival.AirportCode': 1,
        'ScheduleResource.Schedule.Flight.Departure.ScheduledTimeLocal.DateTime': 1,
        'ScheduleResource.Schedule.Flight.MarketingCarrier.AirlineID': 1,
        'ScheduleResource.Schedule.Flight.MarketingCarrier.FlightNumber': 1
    }
    cursor = client[settings.DB_NAME][settings.COLLECTION_NAME].find(query, projection)
    
    flights = []
    seen_flights = set()
    for document in cursor:
        for schedule in document.get('ScheduleResource', {}).get('Schedule', []):
            for flight in schedule.get('Flight', []):
                try:
                    departure_airport = flight['Departure']['AirportCode']
                    arrival_airport = flight['Arrival']['AirportCode']
                    departure_date = flight['Departure']['ScheduledTimeLocal']['DateTime']
                    airline_id = flight['MarketingCarrier']['AirlineID']
                    flight_number = flight['MarketingCarrier']['FlightNumber']
                    
                    # Filter out flights that do not match the departure and arrival airport codes
                    if departure_airport == airport_departure and arrival_airport == airport_arrival:
                        flight_identifier = (departure_airport, arrival_airport, departure_date, airline_id, flight_number)
                        
                        if flight_identifier not in seen_flights:
                            seen_flights.add(flight_identifier)
                            flight_data = Flight(
                                departure_airport=departure_airport,
                                arrival_airport=arrival_airport,
                                departure_date=departure_date,
                                airline_id=airline_id,
                                flight_number=flight_number
                            )
                            flights.append(flight_data)
                except TypeError as e:
                    print('TypeError:', e)
                    continue

    return flights