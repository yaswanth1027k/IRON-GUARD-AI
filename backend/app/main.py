from fastapi import FastAPI

from app.api.routes import api_router
from app.core.config import settings
from app.core.logger import logger

logger.info("Starting IRON GUARD AI")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Industrial Safety Intelligence Platform"
)

app.include_router(
    api_router,
    prefix=settings.API_PREFIX
)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }