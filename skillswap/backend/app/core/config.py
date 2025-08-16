from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str
    JWT_EXPIRES: int = 3600
    DEBUG: bool = True
    MAP_DEFAULT_LAT: float = Field(default=41.8781)
    MAP_DEFAULT_LON: float = Field(default=-87.6298)

    class Config:
        env_file = ".env"

settings = Settings()
