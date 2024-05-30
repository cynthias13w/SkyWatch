from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LH_SECRET: str
    LH_KEY: str
    LH_TOKEN_URL: str
    LH_OPERATIONS_URL: str
    MONGO_CLIENT: str
    MONGO_DB: str
    MONGO_COLLECTION: str
    MAX_CALLS_PER_SECOND: int
    MAX_CALLS_PER_HOUR: int

    class Config:
        env_file = '.env'

settings = Settings()
