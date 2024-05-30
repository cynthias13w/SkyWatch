from pydantic import BaseModel
from typing import Any

# base model for formatting the flights
class Flight(BaseModel):
    departure_airport: Any
    arrival_airport: Any
    departure_date: Any
    airline_id: Any
    flight_number: Any