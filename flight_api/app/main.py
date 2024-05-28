from fastapi import FastAPI
from app.routes import router
from app.config import settings

api = FastAPI()

api.include_router(router)

@api.get('/alive')
def alive():
    return {'status': 'Welcome to the Sky Watch API. The API is working!'}