import configparser
import requests
import pymongo
from pprint import pprint
import reference_data

# API endpoint URL
config = configparser.ConfigParser()
config.read('config.ini')
mongo_client = pymongo.MongoClient(config['MONGO_DB']['MONGO_CLIENT'])
db = mongo_client['SkyWatch']
collection = db['cities']


try:
    data = reference_data.get_cities_data('SAO')
    pprint(data)
    collection.insert_one(data)
    print('Data saved')

except requests.exceptions.RequestException as e:
    print(f"Error occurred during API request: {e}")

finally:
    # Close MongoDB connection
    mongo_client.close()
