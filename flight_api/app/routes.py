from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Flight
from app.services import get_flights, get_flight_count, get_one_flight
from bson import ObjectId


router = APIRouter()

def convert_mongo_to_json(data):
    """Make sure the document is serializable"""
    if isinstance(data, list):
        return [convert_mongo_to_json(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_mongo_to_json(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@router.get('/flight_count')
async def read_flight_count():
    """Return the number of documents in database"""
    flights = await get_flight_count()
    if flights is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return flights


@router.get('/one_flight')
async def read_one_flight():
    """Return one raw document from database"""
    flight = await get_one_flight()
    if flight is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return convert_mongo_to_json(flight)


@router.get('/flights', response_model=List[Flight])
async def read_flights(airport_departure: str, 
                       airport_arrival: str, 
                       date_departure: str):
    """Return formated flights based on given criteria"""
    flights = await get_flights(airport_departure, airport_arrival, date_departure)
    if flights is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return flights


