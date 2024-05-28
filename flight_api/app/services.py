from app.models import Flight
from app.config import settings
from typing import List, Optional
import pymongo

client = pymongo.MongoClient(settings.MONGO_URI)

async def get_flight_count():
    total_count = client[settings.DB_NAME][settings.COLLECTION_NAME].count_documents({})
    return {'flight count': f'{total_count}'}


async def get_one_flight():
    cursor = client[settings.DB_NAME][settings.COLLECTION_NAME].find_one()
    return cursor

async def get_flights(origin: Optional[str] = None, 
                      destiny: Optional[str] = None, 
                      date: Optional[str] = None) -> List[Flight]:
    query = {}
    if origin:
        query['origin'] = origin
    if destiny:
        query['destiny'] = destiny
    if date:
        query['date'] = date

    cursor = client[settings.DB_NAME][settings.COLLECTION_NAME].find(query)
    flights = await cursor.to_list(length=100)
    return [Flight(**flight) for flight in flights]
