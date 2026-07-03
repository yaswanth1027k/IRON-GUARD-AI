from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "IRON GUARD AI"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # PostgreSQL Database Settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # MQTT Broker Settings
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883

    # Dynamically build the database URL
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Changed from postgresql:// to postgresql+asyncpg://
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Load from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

# Instantiate the settings object to be used across the app
settings = Settings()