from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import Flight
from app.services import get_flights, get_flight_count, get_one_flight

router = APIRouter()

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
    return flight


@router.get('/flights', response_model=List[Flight])
async def read_flights(origin: Optional[str] = None, 
                       destiny: Optional[str] = None, 
                       date: Optional[str] = None):
    flights = await get_flights(origin, destiny, date)
    if flights is None:
        raise HTTPException(status_code = 404, detail = 'Flights not found')
    return flights


