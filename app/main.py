from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import adjuntoRouter, cajaRouter, clientesRouter, estudioMedicoRouter, facturaDetalleRouter, facturaRouter, gastoRouter, health, mascotasRouter, movimientoCajaRouter, pagoRouter, recetaMedicamentoRouter, recetaRouter, usuariosRouter, turnosRouter, historiaClinicaRouter, vacunaRouter

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=[
        "*",
    ],
    allow_headers=[
        "*",
    ],
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

app.include_router(
    usuariosRouter.router,
    prefix="/api"
)

app.include_router(
    turnosRouter.router,
    prefix="/api"
)

app.include_router(
    historiaClinicaRouter.router,
    prefix="/api",
)

app.include_router(
    vacunaRouter.router,
    prefix="/api"
)

app.include_router(
    recetaRouter.router,
    prefix="/api"
)

app.include_router(
    recetaMedicamentoRouter.router,
    prefix="/api"
)

app.include_router(
    estudioMedicoRouter.router,
    prefix="/api",
)

app.include_router(
    adjuntoRouter.router,
    prefix="/api"
)

app.include_router(
    facturaRouter.router,
    prefix="/api",
)

app.include_router(
    facturaDetalleRouter.router,
    prefix="/api",
)

app.include_router(
    pagoRouter.router,
    prefix="/api",
)

app.include_router(
    cajaRouter.router,
    prefix="/api",
)

app.include_router(
    movimientoCajaRouter.router,
    prefix="/api",
)

app.include_router(
    gastoRouter.router,
    prefix="/api",
)