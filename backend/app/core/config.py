from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    DEBUG: bool

    HOST: str
    PORT: int

    API_PREFIX: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    MQTT_BROKER: str
    MQTT_PORT: int

    JWT_SECRET: str

    LOG_LEVEL: str

    class Config:
        env_file = ".env"


settings = Settings()