# Flight API

This is a FastAPI application that queries a MongoDB database to return flight information.

## Running the Application

1. Clone the repository.
2. Create a `.env` file with the varibles MONGO_URI, DB_NAME, COLLECTION_NAME
3. Build and start the containers using Docker Compose.
4. There is a test file you can run after the docker container is up

```sh
docker-compose up --build
bash test_api.sh