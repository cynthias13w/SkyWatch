import requests
from config import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_auth_token():
    """
    get the authentication token
    :return: auth token
    """

    # set variables
    secret = settings.LH_SECRET
    key = settings.LH_KEY
    token_url = settings.LH_TOKEN_URL
    data = {'client_id': key, 'client_secret': secret, 'grant_type': 'client_credentials'}

    r = requests.post(token_url, data=data)
    if r.status_code == 200:
        token_string = r.json()
        return token_string['access_token']
    else:
        return 'invalid token'


def get_header():
    """
    getting the header with authorization token
    :return: header for further requests
    """
    token = get_auth_token()
    headers = {'Accept': 'application/json', 'Authorization':f'Bearer {token}'}
    return headers


def test_db_connection():
    # Create a new client and connect to the server
    client = MongoClient(settings.MONGO_CLIENT, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e
