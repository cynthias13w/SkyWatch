#!/bin/bash

# Wait for docker to get the server up
sleep 10

# Check if the API is alive
curl -X 'GET' \
  'http://api:8000/alive' \
  -H 'accept: application/json'

# Get Flight count
curl -X 'GET' \
  'http://api:8000/flight_count' \
  -H 'accept: application/json'

# Get one flight
curl -X 'GET' \
  'http://api:8000/one_flight' \
  -H 'accept: application/json'

# Get formatted flights
curl -X 'GET' \
  'http://api:8000/flights?airport_departure=BER&airport_arrival=MUC&date_departure=2024-07-15' \
  -H 'accept: application/json'
