from pydantic import BaseModel
from datetime import datetime

class Flight(BaseModel):
    origin: str
    destiny: str
    date: datetime
    flight_number: str
    airline: str
