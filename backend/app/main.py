from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.mqtt.subscriber import create_mqtt_client, MQTT_BROKER, MQTT_PORT, latest_readings

mqtt_client = create_mqtt_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    yield
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/v1/mqtt/latest")
def get_latest_mqtt():
    
    return latest_readings