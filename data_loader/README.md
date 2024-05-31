# Data Loader
This script will load data from Lufthansa API into a given Mongo Instance

## How to use this script:
1. Add the necessary conection information to the file `.env` 
    LH_SECRET, LH_KEY, LH_TOKEN_URL, LH_OPERATIONS_URL, MONGO_CLIENT, MONGO_DB, MONGO_COLLECTION, MAX_CALLS_PER_SECOND, MAX_CALLS_PER_HOUR
2. Set up the variables in the file get_flights.py
3. Run the script with python3

```sh
docker build -t data_loader .
docker run --env-file .env data_loader


