import requests
import configparser
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_auth_token(api_key = None):
    """
    get the authentication token
    :return: auth token
    """
    # read config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # set variables
    if (api_key == None) or (api_key == 1):
        secret = config['LH_OPENAPI']['LH_SECRET'] # client secret
        key = config['LH_OPENAPI']['LH_KEY'] # client id
    elif api_key == 2:
        secret = config['LH_OPENAPI_2']['LH_SECRET'] # client secret
        key = config['LH_OPENAPI_2']['LH_KEY'] # client id   
    elif api_key == 3:
        secret = config['LH_OPENAPI_3']['LH_SECRET'] # client secret
        key = config['LH_OPENAPI_3']['LH_KEY'] # client id
    
    token_url = config['LH_OPENAPI']['LH_TOKEN_URL']
    data = {'client_id': key, 'client_secret': secret, 'grant_type': 'client_credentials'}

    r = requests.post(token_url, data=data)
    if r.status_code == 200:
        token_string = r.json()
        return token_string['access_token']
    else:
        return 'invalid token'


def get_header(api_key = None):
    """
    getting the header with authorization token
    :return: header for further requests
    """
    token = get_auth_token(api_key)
    headers = {'Accept': 'application/json', 'Authorization':f'Bearer {token}'}
    return headers


def test_db_connection():
    # read config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create a new client and connect to the server
    client = MongoClient(config['MONGO_DB']['MONGO_CLIENT'], server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e
