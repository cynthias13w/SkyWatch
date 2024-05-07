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

countries = ['DE','FR','IT','AT']
try:
    for country in countries: 
        data = reference_data.get_countries_data(country)
        pprint(data)
        collection.insert_one(data)
        print('Data saved')

except Exception as e:
    print("Error connecting to MongoDB:", e)
finally:
    mongo_client.close()
