from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import clientesRouter, health, mascotasRouter


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.include_router(
    health.router,
    prefix="/api"
)


app.include_router(
    clientesRouter.router,
    prefix="/api"
)

app.include_router(
    mascotasRouter.router,
    prefix="/api"
)