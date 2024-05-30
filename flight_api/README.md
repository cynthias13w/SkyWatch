# Flight API

This is a FastAPI application that queries a MongoDB database to return flight information.

## Running the Application

1. Clone the repository.
2. Create a `.env` file with your MongoDB connection string.
3. Build and start the containers using Docker Compose.

```sh
docker-compose up --build
bash test_api.sh