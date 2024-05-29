from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import Flight
from app.services import get_flights, get_flight_count, get_one_flight
from bson import ObjectId


router = APIRouter()

def convert_mongo_to_json(data):
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
    flights = await get_flight_count()
    if flights is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return flights


@router.get('/one_flight')
async def read_one_flight():
    flight = await get_one_flight()
    if flight is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return convert_mongo_to_json(flight)


@router.get('/flights', response_model=List[Flight])
async def read_flights(origin: Optional[str] = None, 
                       destiny: Optional[str] = None, 
                       date: Optional[str] = None):
    flights = await get_flights(origin, destiny, date)
    if flights is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return convert_mongo_to_json(flights)


