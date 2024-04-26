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
collection = db['countries']


try:
    data = reference_data.get_countries_data('BR')
    pprint(data)
    collection.insert_one(data)
    print('Data saved')

except requests.exceptions.RequestException as e:
    print('Something went wrong!!!')

finally:
    # Close MongoDB connection
    mongo_client.close()
